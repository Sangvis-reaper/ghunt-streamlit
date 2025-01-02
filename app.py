import streamlit as st
import subprocess

def run_ghunt_command(command):
    """Run a GHunt command and capture the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def check_session():
    """Check if a valid session exists for GHunt."""
    output = run_ghunt_command("python3 main.py email test@example.com")
    if "Please generate a new session" in output:
        return False
    return True

def main():
    st.title("GHunt Streamlit Interface")

    # Check Session Validity
    if not check_session():
        st.error("No valid session found. Please authenticate using the 'Login Authentication' option.")

    # Options
    st.sidebar.header("Options")
    task = st.sidebar.selectbox(
        "Select Task",
        ("Login Authentication", "Email Information", "Gaia ID Information", "Drive Information", "Geolocate BSSID")
    )

    if task == "Login Authentication":
        st.header("Login Authentication")
        base64_input = st.text_area("Paste the Base64-encoded authentication string:")
        if st.button("Authenticate with Base64"):
            if base64_input:
                st.info("Authenticating with Base64-encoded string...")
                # Automatically select option 2 and provide the Base64 input
                command = f"echo '2\n{base64_input}\n' | python3 main.py login"
                output = run_ghunt_command(command)
                if "Please generate a new session" in output:
                    st.error("Authentication failed. Ensure your Base64 string is correct and try again.")
                else:
                    st.success("Authentication successful!")
                st.text_area("Output:", output, height=300)
            else:
                st.warning("Please provide a Base64-encoded authentication string.")

    elif task == "Email Information":
        st.header("Email Information")
        email = st.text_input("Enter the email address to investigate:")

        if st.button("Run GHunt on Email"):
            if email:
                st.info("Running GHunt on the provided email...")
                output = run_ghunt_command(f"python3 main.py email {email}")
                if "Please generate a new session" in output:
                    st.error("Session invalid. Please authenticate first using the 'Login Authentication' option.")
                st.text_area("Output:", output, height=300)
            else:
                st.warning("Please provide a valid email address.")

    elif task == "Gaia ID Information":
        st.header("Gaia ID Information")
        gaia_id = st.text_input("Enter the Gaia ID to investigate:")

        if st.button("Run GHunt on Gaia ID"):
            if gaia_id:
                st.info("Running GHunt on the provided Gaia ID...")
                output = run_ghunt_command(f"python3 main.py gaia {gaia_id}")
                if "Please generate a new session" in output:
                    st.error("Session invalid. Please authenticate first using the 'Login Authentication' option.")
                st.text_area("Output:", output, height=300)
            else:
                st.warning("Please provide a valid Gaia ID.")

    elif task == "Drive Information":
        st.header("Drive Information")
        drive_url = st.text_input("Enter the Drive file or folder URL:")

        if st.button("Run GHunt on Drive URL"):
            if drive_url:
                st.info("Running GHunt on the provided Drive URL...")
                output = run_ghunt_command(f"python3 main.py drive {drive_url}")
                if "Please generate a new session" in output:
                    st.error("Session invalid. Please authenticate first using the 'Login Authentication' option.")
                st.text_area("Output:", output, height=300)
            else:
                st.warning("Please provide a valid Drive URL.")

    elif task == "Geolocate BSSID":
        st.header("Geolocate BSSID")
        bssid = st.text_input("Enter the BSSID to geolocate:")

        if st.button("Run GHunt on BSSID"):
            if bssid:
                st.info("Geolocating the provided BSSID...")
                output = run_ghunt_command(f"python3 main.py geolocate {bssid}")
                if "Please generate a new session" in output:
                    st.error("Session invalid. Please authenticate first using the 'Login Authentication' option.")
                st.text_area("Output:", output, height=300)
            else:
                st.warning("Please provide a valid BSSID.")

if __name__ == "__main__":
    main()
