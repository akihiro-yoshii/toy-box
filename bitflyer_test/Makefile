CANDLE_MINUTE=1
CANDLE=
# CANDLE=--plot_candle

.PHONY: all
all: simulate candle

simulate: candle.csv
	python src/simulate.py candle.csv simulate_result.txt --test_iter 1000 --thread_size 8
	python src/simulate2graph.py simulate_result.txt simulate_result.png

candle: candle.csv
	python src/candle2picture.py candle.csv images/chart_3month.png --output_length 129600 --roll_spans 1440 7200 21600
	python src/candle2picture.py candle.csv images/chart_month.png --output_length 43200 --roll_spans 360 1440 7200
	python src/candle2picture.py candle.csv images/chart_week.png --output_length 10080 --roll_spans 60 360 1440
	python src/candle2picture.py candle.csv images/chart_day.png --output_length 1440 --roll_spans 15 60 360

candle.csv: data/executions
	python src/executions2candle.py data/executions candle.csv --span ${CANDLE_MINUTE}

FORCE:

.PHONY: clean
clean:
	rm -f candle.csv
