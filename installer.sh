#!/bin/bash

check_and_install_python_on_mac() {
    # Check if we are on macOS
    if [[ $(uname) == "Darwin" ]]; then
        echo "Detected macOS..."

        # Check if brew is installed
        if ! command -v brew &>/dev/null; then
            echo "Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            wait
        else
            echo "Homebrew is already installed."
        fi

        # Check if python3 is installed
        if ! command -v python3 &>/dev/null; then
            echo "python3 not found. Installing..."
            brew install python3
        else
            echo "python3 is already installed."
        fi

        # Check if tcl-tk is installed
        if ! brew list tcl-tk &>/dev/null; then
            echo "tcl-tk is not installed. Installing now..."
            brew install tcl-tk
        else
            echo "tcl-tk is already installed."
            brew uninstall tcl-tk
            brew install tcl-tk
        fi

        # Check if pip3 is installed
        if ! command -v pip3 &>/dev/null; then
            echo "pip3 not found. Installing..."
            brew install pip3
        else
            echo "pip3 is already installed."
        fi
    fi
}

check_and_install_python_on_mac

# Spinner animation
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Check for internet connection
if ! ping -c 1 8.8.8.8 &>/dev/null; then
    echo "No internet connection. Please check your connection and try again."
    exit 1
fi

# Base directory
BASE_DIR=~/SmartFPS

# Check if it's a fresh install or an update
if [[ -d "${BASE_DIR}/SmartFingerprintScanner-main" ]]; then
    UPDATE=true
else
    UPDATE=false
fi

# Display messages in big font
display_message() {
    echo -e "\n\n"
    echo "##################################################"
    echo "#                                                #"
    echo "#                 $1                 #"
    echo "#                                                #"
    echo "##################################################"
    echo -e "\n\n"
}

# Start message
if [ "$UPDATE" = true ]; then
    display_message "Updating SmartFingerprintScanner"
else
    display_message "Installing SmartFingerprintScanner"
fi

# Create the base directory if it doesn't exist
mkdir -p "${BASE_DIR}"

# Download and extract the repositories
download_and_extract() {
    local repo_url="$1"
    local folder_name="$2"
    local output_zip="${BASE_DIR}/${folder_name}.zip"

    # Download the repository
    curl -s -L "${repo_url}" -o "${output_zip}" &

    # Start the spinner animation
    spinner $! &

    # Wait for download to complete
    wait

    # Extract the repository
    unzip -o -q "${output_zip}" -d "${BASE_DIR}"
    rm "${output_zip}" # Remove the downloaded zip file
}

# Download and extract repositories in parallel
download_and_extract "https://github.com/Nauman3S/SmartFingerprintScanner/archive/refs/heads/main.zip" "SmartFingerprintScanner" &

# Wait for the download to complete
wait

# Clean up and setup GUI
cd "${BASE_DIR}/SmartFingerprintScanner-main"

# Check if requirements are already installed
if ! pip3 freeze | grep -q -f GUI/requirements.txt; then
    pip3 install -r GUI/requirements.txt &
    spinner $! &
    wait
fi

chmod +x run.sh

# End message
if [ "$UPDATE" = true ]; then
    display_message "SmartFingerprintScanner Updated"
else
    display_message "SmartFingerprintScanner Installed"
fi
