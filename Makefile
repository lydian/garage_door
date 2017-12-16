
install:
	sudo cp garage_door.service /etc/systemd/system/

debug:
	FLASK_APP=web.py FLASK_DEBUG=1 flask run --host=0.0.0.0

