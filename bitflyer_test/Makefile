DATA_LENGTH=360
SPAN_MINUTE=1
CANDLE=--plot_candle
# CANDLE=

.PHONY: all
all: test.png

test.png: test.csv
	python src/candle2picture.py test.csv test.png --output_length $(DATA_LENGTH) ${CANDLE}

test.csv: FORCE
	python src/executions_to_minute_data.py test.csv --span ${SPAN_MINUTE}

FORCE:

.PHONY: clean
clean:
	rm -f test.csv test.png
