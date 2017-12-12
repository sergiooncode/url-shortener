test:
	URL_SHORTENER_SETTINGS=`pwd`/config/test.py source venv/bin/activate && nose2 -s . tests -v 
