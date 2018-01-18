import os
from itertools import chain
from preprocessors.nop import Nop
from preprocessors.token_processor import *
from comparators.winnowing import Winnowing
# map file extensions to lists of (preprocessor, comparator, weight) triples
CONFIG = {
    ".py": [
        (TokenProcessor(
            "Python3",
            StripWhitespace()),
         Winnowing(16, 32), 1),
        (TokenProcessor(
            "Python3",
            StripWhitespace(),
            StripComments(),
            NormalizeIdentifiers(),
            NormalizeStringLiterals()),
         Winnowing(10, 20), 1)
    ],
    ".c": [
        (TokenProcessor(
            "C",
            StripWhitespace()),
         Winnowing(16, 32), 1),
        (TokenProcessor(
            "C",
            StripWhitespace(),
            StripComments(),
            NormalizeIdentifiers(),
            NormalizeStringLiterals()),
         Winnowing(10, 20), 1)
    ],
    "default": [
        (Nop(), Winnowing(20, 40))
    ]
}


def compare(distro, submissions, corpus=[]):
    """Compares a group of submissions to each other and to an optional
    other corpus. Returns an ordered list of Results."""

    def by_extension(entries):
        results = {}
        for file, sub in entries:
            _, ext = os.path.splitext(file)
            if ext not in CONFIG.keys():
                ext = "default"
            results.setdefault(ext, []).append((file, sub))
        return results

    # pair each file with its submission index and split by extension
    distro_files = by_extension((file, distro) for file in distro)
    sub_files = by_extension(chain(*[[(file, sub) for file in sub]
                                     for sub in submissions]))
    corpus_files = by_extension(chain(*[[(file, sub) for file in sub]
                                        for sub in corpus]))

    # get deterministic ordering of extensions
    extensions = list(set(distro_files.keys()) |
                      set(sub_files.keys()) |
                      set(corpus_files.keys()))

    def indices(files):
        indices = {ext: [] for ext in extensions}
        for ext in extensions:
            files = files.setdefault(ext, [])
            for preprocessor, comparator, weight in CONFIG[ext]:
                index = comparator.empty_index()
                for file in files:
                    index += comparator.create_index(*file, preprocessor)
                indices[ext].append((index, weight))
        return indices

    # create (index, weight) pairs for used file types
    distro_indices = indices(distro_files)
    sub_indices = indices(sub_files)
    corpus_indices = indices(corpus_files)

    # remove distro data from submissions
    for ext in extensions:
        index_sets = zip(distro_indices[ext],
                         sub_indices[ext],
                         corpus_indices[ext])
        for (distro_idx, _), (sub_idx, _), (corpus_idx, _) in index_sets:
            sub_idx -= distro_idx
            corpus_idx += sub_idx
            corpus_idx -= distro_idx

    # perform comparisons
    results = dict()
    for ext in extensions:
        index_pairs = zip(sub_indices[ext], corpus_indices[ext])
        for (sub_idx, _), (corpus_idx, _) in index_pairs:
            for sub_pair, score, span_pairs in sub_idx.compare(corpus_idx):
                entry = results.setdefault(sub_pair, dict())
                entry.setdefault(ext, []).append((score, span_pairs))

    # TODO: combine exts within each submission? use weights?
    return results