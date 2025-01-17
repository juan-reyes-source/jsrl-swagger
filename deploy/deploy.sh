BRANCH=$1

install_python_requirements () {
    pip3 install -r requirements.txt
}

delete_dist () {
    rm -f dist/*.whl
}

generate_wheel_file () {
    python3 -m venv venv
    source venv/bin/activate
    
    pip freeze
    pip3 install -r requirements.txt
    pip freeze
    
    cd ..
    python3 -B setup.py bdist_wheel

    rm -r build/
    
    cd deploy
    deactivate
    rm -r venv
}

main () {
    cd ..
    delete_dist
    cd deploy
    generate_wheel_file
}

main