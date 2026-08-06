export UPLOAD_EMAIL ?= n.sastry@surrey.ac.uk

# lib/ghpages.mk deletes any top-level directory on gh-pages that is not
# also a branch name once it is GHPAGES_BRANCH_TTL days old, and registry/
# qualifies. Opt out rather than relying on the site being rebuilt often.
export GHPAGES_BRANCH_TTL := 36500

LIBDIR := lib
-include $(LIBDIR)/main.mk

# lib/deps.mk points BUNDLE_PATH at lib/.gems relative to the repo root, and
# warns that it does so. Bundler resolves a relative BUNDLE_PATH against the
# Gemfile's own directory, which is lib/, so it looks in lib/lib/.gems, finds
# nothing, and every kramdown-rfc run dies on a missing gem. An absolute path
# is unambiguous wherever it is read from.
BUNDLE_PATH := $(CURDIR)/$(LIBDIR)/.gems

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
