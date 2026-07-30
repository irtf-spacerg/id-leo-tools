export UPLOAD_EMAIL ?= n.sastry@surrey.ac.uk

LIBDIR := lib
-include $(LIBDIR)/main.mk

$(LIBDIR)/main.mk:
ifneq (,$(shell grep "path *= *$(LIBDIR)" .gitmodules 2>/dev/null))
	git submodule sync
	git submodule update --init
else
ifneq (,$(wildcard $(ID_TEMPLATE_HOME)))
	ln -s "$(ID_TEMPLATE_HOME)" $(LIBDIR)
else
	git clone -q --depth 10 -b main \
	    https://github.com/martinthomson/i-d-template $(LIBDIR)
endif
endif

# ------------------------------------------------------------------- prose --
# Lay the draft out one sentence per line (mirrors id-leo-constellations).
# Idempotent. One sentence per line keeps review diffs to what changed.
FILES ?=
.PHONY: fmt fmt-wrap fmt-check
fmt:
	python3 scripts/reflow.py --sentences $(FILES)

fmt-wrap:
	python3 scripts/reflow.py $(FILES)

fmt-check:
	python3 scripts/reflow.py --sentences --check $(FILES)
