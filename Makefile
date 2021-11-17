clean:
	@echo "Cleaning up..."
	rm ./Data/streaming/*
	rm ./Data/song/*
	rm ./Data/art/*
	rm ./Data/beat/*
	rm ./Data/lyric/*
	rm ./Data/composer/*
	rm ./Data/genre/*
	rm ./error.txt
	touch ./error.txt
	@echo "Done cleaning"

crawl:
	@echo "Crawling..."
	python main.py

