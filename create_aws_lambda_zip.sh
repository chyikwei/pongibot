ROOT_DIR=${PWD}
ZIP_PATH="${PWD}/pongibot_v0.0.1.zip"

zip -j9 ${ZIP_PATH} *.py

cd "${PWD}/venv_bot/lib/python2.7/site-packages/"
zip -r9 ${ZIP_PATH} *

cd ${ROOT_DIR}