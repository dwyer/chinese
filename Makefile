CEDICT_TXT2DB=cedict_txt2db.py

CEDICT_DB=cedict.db
CEDICT_TXT=cedict_1_0_ts_utf-8_mdbg.txt
CEDICT_TXT_GZ=$(CEDICT_TXT).gz
CEDICT_TXT_GZ_URL=http://www.mdbg.net/chindict/export/cedict/$(CEDICT_TXT_GZ)

all: $(CEDICT_DB)

$(CEDICT_DB): $(CEDICT_TXT) $(CEDICT_TXT2DB)
	./$(CEDICT_TXT2DB) $(CEDICT_TXT) $(CEDICT_DB)

$(CEDICT_TXT):
	curl -O $(CEDICT_TXT_GZ_URL)
	gunzip $(CEDICT_TXT_GZ)

clean:
	$(RM) $(CEDICT_DB) $(CEDICT_TXT) $(CEDICT_TXT_GZ)
