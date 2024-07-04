
pdm() {
  local command=$1

  if [[ "$command" == "shell" ]]; then
    # Check if pdm is installed
    if ! command -v pdm &> /dev/null; then
      echo "PDM is not installed. Please install PDM first."
      return 1
    fi

    # Fetch the PDM virtual environment activation command
    local activation_command=$(command pdm venv activate 2> /dev/null)

    # Check if the PDM virtual environment exists and can be activated
    if [[ -z "$activation_command" ]]; then
      echo "No PDM virtual environment found. Please ensure a virtual environment is created."
      return 1
    fi

    # Add a debug print before eval
    eval "source $activation_command"
    echo "PDM virtual environment activated."
    echo "Use command 'deactivate' to exit the virtual environment."
  else
    command pdm $@
  fi
}


# Usage instruction to be displayed to the user
echo "Customized 'pdm' via bash function. Run 'pdm shell' to activate the PDM virtual environment."
