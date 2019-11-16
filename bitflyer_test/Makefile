DATA_LENGTH=240
SPAN_MINUTE=60
CANDLE=--plot_candle
# CANDLE=

.PHONY: all
all: test.png

test.png: test.csv
	python src/candle2picture.py test.csv test.png --output_length $(DATA_LENGTH) ${CANDLE}

test.csv:
	python src/executions_to_minute_data.py test.csv --span ${SPAN_MINUTE}

.PHONY: clean
clean:
	rm -f test.csv test.png
