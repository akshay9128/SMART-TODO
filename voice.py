import requests
import speech_recognition as sr
import time


BASE_URL = "http://127.0.0.1:8000"

USERNAME = "user1"
PASSWORD = "123456"

DEVICE_INDEX = 1


def login():
    print("\nLogging in...")

    response = requests.post(
        f"{BASE_URL}/users/login",
        data={
            "username": USERNAME,
            "password": PASSWORD,
        },
    )

    print("Login HTTP Status:", response.status_code)

    if response.status_code != 200:
        print("Login failed:")
        print(response.text)
        return None

    data = response.json()

    token = data.get("access_token")

    if not token:
        print("No access token received.")
        print(data)
        return None

    print("Login successful.")
    print("Access token received.")

    return token


def listen():
    recognizer = sr.Recognizer()

    print("\nOpening microphone:")
    print("Using Microphone Device:",DEVICE_INDEX)

    print("\nOpening microphone...")

    try:
        with sr.Microphone(device_index=DEVICE_INDEX) as source:

            print("Microphone opened.")

            print("Calibrating...")
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = False

            print("\n" + "=" * 55)
            print("🎤 SPEAK NOW")
            print("=" * 55)

            print("Speak your command.")
            print()

            time.sleep(1)

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=8
            )

            print("\nRecording finished.")
            print("Recognizing...")

    except sr.WaitTimeoutError:
        print("Timed out. No speech detected.")
        return None

    except Exception as e:
        print("Microphone error:", e)
        return None

    try:
        text = recognizer.recognize_google(audio)

        print("\nYOU SAID:")
        print(text)

        return text

    except sr.UnknownValueError:
        print("\nCould not understand the speech.")

        try:
            with open("voice_debug.wav", "wb") as f:
                f.write(audio.get_wav_data())

            print("Saved recording to voice_debug.wav")

        except Exception as e:
            print("Could not save audio:", e)

        return None

    except sr.RequestError as e:
        print("\nSpeech recognition service error:")
        print(e)
        return None


def send_to_agent(text, token, confirmed=False):

    print("\nSending to AI Agent...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "confirmed": confirmed,
    }

    print("\nRequest body:")
    print(payload)

    response = requests.post(
        f"{BASE_URL}/agent/",
        json=payload,
        headers=headers,
        timeout=30,
    )

    print("HTTP Status:", response.status_code)

    try:
        agent_response = response.json()
        print(agent_response.get("message",agent_response))
        # print("\nAI AGENT RESPONSE:")
        # print(agent_response)

        return agent_response

    except Exception:
        print("\nRaw response:")
        print(response.text)
        return None


def is_confirmation(text):

    text = text.lower().strip()

    confirmation_words = [
        "yes",
        "yes delete it",
        "yes delete",
        "delete it",
        "confirm",
        "confirm delete",
        "yes please",
        "yes please delete it",
    ]

    return text in confirmation_words


def main():

    print("=" * 55)
    print("VOICE → AI AGENT TEST")
    print("=" * 55)

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    token = login()

    if not token:
        print("\nStopping because login failed.")
        return

    # --------------------------------------------------
    # FIRST VOICE COMMAND
    # --------------------------------------------------

    text = listen()

    if not text:
        print("\nNo text was produced.")
        print("AI Agent was NOT called.")
        print("\nTest finished.")
        return

    # --------------------------------------------------
    # SEND NORMAL REQUEST
    # --------------------------------------------------

    agent_response = send_to_agent(
        text=text,
        token=token,
        confirmed=False
    )

    if not agent_response:
        print("\nNo response from AI Agent.")
        print("\nTest finished.")
        return

    # --------------------------------------------------
    # CHECK FOR DELETE CONFIRMATION
    # --------------------------------------------------

    if agent_response.get("requires_confirmation"):

        pending_delete_task_id = agent_response.get("task_id")

        print("\n" + "=" * 55)
        print("⚠️ DELETE CONFIRMATION REQUIRED")
        print("=" * 55)

        print(
            f"Task ID waiting for confirmation: "
            f"{pending_delete_task_id}"
        )

        print("\nThe task has NOT been deleted.")

        # --------------------------------------------------
        # LISTEN FOR CONFIRMATION
        # --------------------------------------------------

        print("\nPlease confirm the deletion.")

        confirmation_text = listen()

        if not confirmation_text:

            print("\nNo confirmation received.")
            print("Task was NOT deleted.")
            print("\nTest finished.")
            return

        print("\nCONFIRMATION:")
        print(confirmation_text)

        # --------------------------------------------------
        # CHECK CONFIRMATION
        # --------------------------------------------------

        if is_confirmation(confirmation_text):

            print("\nConfirmation accepted.")

            print(
                f"Deleting task "
                f"{pending_delete_task_id}..."
            )

            # IMPORTANT:
            # We use the remembered task ID.
            #
            # The user does NOT need to say:
            # "yes delete task 54"
            #
            # They can simply say:
            # "yes delete it"

            delete_text = (
                f"delete task {pending_delete_task_id}"
            )

            delete_response = send_to_agent(
                text=delete_text,
                token=token,
                confirmed=True
            )

            if delete_response:

                print("\nFINAL DELETE RESPONSE:")
                print(delete_response)

                if delete_response.get("success"):

                    print(
                        f"\n✅ Task "
                        f"{pending_delete_task_id} "
                        f"was deleted successfully."
                    )

                else:

                    print(
                        "\n❌ Task was not deleted."
                    )

        else:

            print("\nDeletion cancelled.")
            print("Task was NOT deleted.")

    print("\nTest finished.")


if __name__ == "__main__":
    main()