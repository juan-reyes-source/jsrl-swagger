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

update_tag_version_code () {
    cd ..
    library_version=v$(python3 -B -c "from setup import LIBRARY_VERSION;print(LIBRARY_VERSION)")
    echo $library_version
    git tag -d $library_version
    git tag $library_version

    git push origin :$library_version
    git push origin $library_version

    git fetch --tags
}


main () {
    update_tag_version_code
}

main