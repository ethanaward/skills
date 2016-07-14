for f in *; do
    if [[ -d $f ]]; then
        pip install -r "$f/requirements.txt"
        if [ "$f" != "mycroft-core" ]; then
            cp -r $f mycroft-core/mycroft/skills/$f
        fi
    fi
done
