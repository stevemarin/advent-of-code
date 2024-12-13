
.PHONY: run-all day% clean

day%:
	python -m advent_of_code_2024.$@

run-all:
	@for filename in src/advent_of_code_2024/day*; do										\
		echo -n Running: $$(basename $$filename)...;										\
		utime="$$(																			\
			TIMEFORMAT='%lU'; 																\
			time ( python -m advent_of_code_2024.$$(basename $$filename) ) 2>&1 1>/dev/null	\
		)";																					\
		echo " took $${utime}";																\
	done

clean:
	find src/ -type d -name __pycache__ -exec rm -rf {} \;
