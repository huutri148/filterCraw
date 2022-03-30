clean:
	@echo "Cleaning up..."
	rm -rfv ./Data/art/*
	rm -rfv ./Data/genre/*
	rm -rfv ./Data/album/*
	rm -rfv ./Data/type/*
	rm ./total.txt
	rm ./Data/genre.txt
	rm ./Data/type.txt	
	rm ./Data/streaming/*
	rm ./Data/song/*
	rm ./Data/beat/*
	rm ./Data/lyric/*
	#rm ./Data/composer/*
	rm ./error.txt
	touch ./error.txt
	@echo "Done cleaning"

crawl:
	@echo "Crawling..."
	python main.py

