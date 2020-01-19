CANDLE_MINUTE=1
THREAD_SIZE=4
SIMULATE_ITER=1000

.PHONY: all
all: simulate candle

simulate: candle.csv
	python src/simulate.py candle.csv result/simulate_result.txt --test_iter ${SIMULATE_ITER} --thread_size ${THREAD_SIZE}
	python src/simulate2graph.py result/simulate_result.txt result/simulate_result.png

candle: candle.csv
	python src/candle2picture.py candle.csv images/chart_3month.png --output_length 129600 --roll_spans 1440 7200 21600
	python src/candle2picture.py candle.csv images/chart_month.png --output_length 43200 --roll_spans 360 1440 7200
	python src/candle2picture.py candle.csv images/chart_week.png --output_length 10080 --roll_spans 60 360 1440
	python src/candle2picture.py candle.csv images/chart_day.png --output_length 1440 --roll_spans 15 60 360

candle.csv: data/executions
	python src/executions2candle.py data/executions candle.csv --span ${CANDLE_MINUTE}

.PHONY: clean
clean:
	rm -f candle.csv
