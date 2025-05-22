.PHONY: all ltlformulas traces hoa-files traces hoax-traces experiments

# GNU Awk required. Change this to "gawk" on MacOS
# Gawk may be installed e.g. via Homebrew
AWK := gawk 

LTL = 2locks2threads/2locks2threads.ltl.txt 4locks4threads/4locks4threads.ltl.txt 
TRACES = \
	2locks2threads/2locks2threads.50k.txt \
	2locks2threads/2locks2threads.100k.txt \
	2locks2threads/2locks2threads.200k.txt \
	4locks4threads/4locks4threads.50k.txt \
	4locks4threads/4locks4threads.100k.txt \
	4locks4threads/4locks4threads.200k.txt \
	8locks8threads/8locks8threads.50k.txt \
	8locks8threads/8locks8threads.100k.txt \
	8locks8threads/8locks8threads.200k.txt

HOAX_TRACES = $(subst .txt,.hoax.txt,$(TRACES))

all: ltlformulas hoa-files traces hoax-traces
ltlformulas: $(LTL)
traces: $(TRACES)
hoax-traces: $(HOAX_TRACES)
experiments: experiments.log

$(LTL):
	@uv run gen_ltl.py $(shell echo $@ | head -c1 ) > $@

$(TRACES):
	@uv run gen_trace.py $(shell echo $@ | sed 's/[^.]*\.\(.*\)k.txt/\1/')000 $(shell echo $@ | head -c1 ) > $@

$(HOAX_TRACES): $(TRACES)
	@uv run convert_trace.py $(subst .hoax.txt,.txt,$@) $(shell echo $@ | head -c1 ) > $@

hoa-files: ltlformulas
	@mkdir -p 2locks2threads
	@ltl2tgba --negate -SCD -F  2locks2threads/2locks2threads.ltl.txt |  $(AWK) '/HOA: v1/{n++}{print >"2locks2threads/aut" n ".hoa" }'
	@mkdir -p 4locks4threads
	@ltl2tgba --negate -SCD -F  4locks4threads/4locks4threads.ltl.txt |  $(AWK) '/HOA: v1/{n++}{print >"4locks4threads/aut" n ".hoa" }'
	@mkdir -p 8locks8threads
	@ltl2tgba --negate -SCD -F  8locks8threads/8locks8threads.ltl.txt |  $(AWK) '/HOA: v1/{n++}{print >"8locks8threads/aut" n ".hoa" }'

experiments.log:
	@uv run main.py 2> $@
