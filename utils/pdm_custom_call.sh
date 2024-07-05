# Customizes the 'pdm' command to enhance functionality within a bash environment.
# Source this file into your running shell OR do it from your .bashrc or .bash_profile file.

pdm() {
  local command=$1
  if [[ "$command" == "shell" ]]; then
    # Verify if PDM is installed by checking its presence in the system's PATH.
    if ! command -v pdm &> /dev/null; then
      echo "PDM is not installed. Please install PDM first."
      return 1
    fi
    # Attempt to fetch the PDM virtual environment activation command.
    local activation_command=$(command pdm venv activate 2> /dev/null)
    if [[ -z "$activation_command" ]]; then
      echo "No PDM virtual environment found. Please ensure a virtual environment is created."
      return 1
    fi
    eval "source $activation_command"
    echo "PDM virtual environment activated."
    echo "Use command 'deactivate' to exit the virtual environment."
  else
    command pdm $@
  fi
}

# Display usage instructions to the user.
echo "Customized 'pdm' via bash function. Run 'pdm shell' to activate the PDM virtual environment."
