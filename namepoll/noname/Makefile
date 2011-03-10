PO="locale/fr/LC_MESSAGES/django.po"
MO=$(PO:.po=.mo)
makemessages=django-admin.py makemessages
compilemessages=django-admin.py compilemessages

all:		$(MO)

$(MO):	$(PO)
	$(makemessages) -l fr
	$(compilemessages) -l fr

clean:
	@echo $(PO)
	rm -f $(MO)

