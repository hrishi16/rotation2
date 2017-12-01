CHAIN:=12
PSADIR=../../toplot/

PICKLE:=$(CHAIN)_chain.pickle

all : download analyze plot 
	@echo "All done"

download : $(PICKLE) 
	

$(PICKLE) : ./download_chain.py
	python $< $(CHAIN)


analyze : 
	echo "nothing to do here"


plot : ./plot_asa_vs_ne.py $(PICKLE) 
	python $< $(PICKLE) $(PSADIR)
