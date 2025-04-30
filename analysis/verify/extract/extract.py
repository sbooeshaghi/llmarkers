from collections import defaultdict

# from itertools import product
import unicodedata
from unidecode import unidecode

import tiktoken
import re


def norm_text(text):
    """
    Normalize text to ensure UTF-8 compatibility for NLP processing.

    This function:
    1. Normalizes Unicode to the NFC form
    2. Replaces problematic characters with ASCII equivalents
    3. Handles common special characters that cause issues

    Args:
        text (str): Input text to normalize

    Returns:
        str: Normalized text safe for UTF-8 processing
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except:
            return ""

    # Step 1: Unicode normalization to NFC form (composed form)
    # This combines characters and diacritics when possible
    text = unicodedata.normalize("NFC", text)
    text = unidecode(text)

    # Step 2: Map specific problematic characters to ASCII equivalents
    # char_map = {
    #     "ɛ": "e",  # epsilon
    #     "ɑ": "a",  # alpha
    #     "β": "b",  # beta
    #     "δ": "d",  # delta
    #     "γ": "g",  # gamma
    #     "λ": "l",  # lambda
    #     "μ": "u",  # mu
    #     "π": "pi",  # pi
    #     "θ": "theta",  # theta
    #     "τ": "t",  # tau
    #     "ω": "omega",  # omega
    #     "′": "'",  # prime
    #     "″": '"',  # double prime
    #     "–": "-",  # en dash
    #     "—": "--",  # em dash
    #     """: "'",        # curly single quote
    #     """: "'",  # curly single quote
    #     '"': '"',  # curly double quote
    #     '"': '"',  # curly double quote
    #     "…": "...",  # ellipsis
    #     "•": "*",  # bullet
    #     "·": ".",  # middle dot
    #     "×": "x",  # multiplication sign
    #     "÷": "/",  # division sign
    #     "≤": "<=",  # less than or equal
    #     "≥": ">=",  # greater than or equal
    #     "≠": "!=",  # not equal
    #     "≈": "~",  # approximately equal
    #     "∞": "inf",  # infinity
    #     "∂": "d",  # partial differential
    #     "∫": "integral",  # integral
    #     "∑": "sum",  # sum
    #     "∏": "product",  # product
    #     "√": "sqrt",  # square root
    #     "∝": "prop to",  # proportional to
    #     "∠": "angle",  # angle
    #     "△": "triangle",  # triangle
    #     "□": "square",  # square
    #     "∈": "in",  # element of
    #     "∉": "not in",  # not an element of
    #     "⊂": "subset",  # subset
    #     "⊃": "superset",  # superset
    #     "∪": "union",  # union
    #     "∩": "intersect",  # intersection
    #     "⊆": "subseteq",  # subset or equal
    #     "⊇": "superseteq",  # superset or equal
    #     "Π": "Pi",  # uppercase pi
    #     "⁄": "/",  # fraction slash
    #     "½": "1/2",
    #     "⅓": "1/3",
    #     "⅔": "2/3",
    #     "¾": "3/4",
    #     "⅕": "1/5",
    #     "⅖": "2/5",
    #     "⅗": "3/5",
    #     "⅘": "4/5",
    #     "⅙": "1/6",
    #     "⅚": "5/6",
    #     "⅛": "1/8",
    #     "⅜": "3/8",
    #     "⅝": "5/8",
    #     "⅞": "7/8",
    #     "ὀ": "o",  # omicron with smooth breathing
    #     "ξ": "x",  # xi
    #     "ύ": "y",  # upsilon with tonos
    #     "ς": "s",  # final sigma
    #     "ε": "e",  # epsilon
    #     "ν": "n",  # nu
    #     "ή": "e",  # eta with tonos
    #     "ἄ": "a",  # alpha with smooth breathing and tonos
    #     "ζ": "z",  # zeta
    #     "ο": "o",  # omicron
    #     "ᵻ": "i",  # Latin letter with stroke
    #     "ɒ": "a",  # turned alpha
    #     "ə": "e",  # schwa
    #     "ɔ": "o",  # open-mid back rounded vowel
    #     "ː": ":",  # IPA length mark
    #     "κ": "k",  # kappa
    #     "ί": "i",  # iota with tonos
    #     "φ": "ph",  # phi
    #     "ω": "o",  # omega
    # }

    char_map = {
        "–": "-",  # en dash
        "—": "--",  # em dash
        "‘": "'",  # left single quote
        "’": "'",  # right single quote
        "“": '"',  # left double quote
        "”": '"',  # right double quote
        "…": "...",  # ellipsis
        "•": "*",  # bullet
        "·": ".",  # middle dot
        "×": "x",  # multiplication sign
        "÷": "/",  # division sign
        "≤": "<=",  # less than or equal
        "≥": ">=",  # greater than or equal
        "≠": "!=",  # not equal
        "≈": "~",  # approximately equal
        "∞": "inf",  # infinity
        "∂": "d",  # partial differential
        "∫": "integral",  # integral
        "∑": "sum",  # sum
        "∏": "product",  # product
        "√": "sqrt",  # square root
        "∝": "prop to",  # proportional to
        "∠": "angle",  # angle
        "△": "triangle",  # triangle
        "□": "square",  # square
        "∈": "in",  # element of
        "∉": "not in",  # not an element of
        "⊂": "subset",  # subset
        "⊃": "superset",  # superset
        "∪": "union",  # union
        "∩": "intersect",  # intersection
        "⊆": "subseteq",  # subset or equal
        "⊇": "superseteq",  # superset or equal
    }

    for char, replacement in char_map.items():
        text = text.replace(char, replacement)
    # Step 3: Remove any remaining non-ASCII characters (optional)
    # Uncomment if you want to remove ALL non-ASCII characters
    # text = re.sub(r'[^\x00-\x7F]+', '', text)

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)  # .strip()

    return text


def tokenize_with_offsets(text, encoding="cl100k_base"):
    """Tokenizes text and returns tokens with their character start positions."""
    enc = tiktoken.get_encoding(encoding)
    tokens = []

    etks = enc.encode(text)
    dtks, ptks = enc.decode_with_offsets(etks)

    assert len(etks) == len(ptks)

    for t, p in zip(etks, ptks):
        token = enc.decode_single_token_bytes(t).decode("utf-8")
        tobj = {
            "token": token,
            "enc_token": t,
            "start_idx": p,
            "end_idx": p + len(token),
        }
        tokens.append(tobj)
    return tokens


def tokenize(text):
    nt = norm_text(text)
    tks = tokenize_with_offsets(nt)
    t2w = defaultdict(list)
    for tk in tks:
        t2w[tk["enc_token"]].append(tk)
    return (tks, t2w)


def build_index(text, k=1):
    tokens, t2w = tokenize(text)
    ngram_to_id = {}  # Maps n-grams to unique IDs
    id_to_ngram = {}  # Map unique IDs to n-grams
    ngram_id_to_pos = defaultdict(list)  # Positions of each n-gram id
    ngrams = []  # actual list of ngrams (and corresponding tokens)
    counter = 0

    enc_tokens = [i["enc_token"] for i in tokens]

    for i in range(len(enc_tokens) - k + 1):
        ngram = tuple(enc_tokens[i : i + k])  # encoded tuple of tokens

        # get the ngram id or add it
        if ngram not in ngram_to_id:
            ngram_to_id[ngram] = counter
            id_to_ngram[counter] = ngram
            counter += 1
        ngram_id = ngram_to_id[ngram]

        ngram_id_to_pos[ngram_id].append(i)

        ngrams.append({"ngram_id": ngram_id, "tks": tokens[i : i + k]})

    return (ngram_to_id, id_to_ngram, ngram_id_to_pos, ngrams)


def align_target(target, ngram_to_id, ngram_id_to_pos, k=1):
    tokens, t2w = tokenize(target)

    enc_tokens = [i["enc_token"] for i in tokens]

    aln = []

    prev_id = None
    for i in range(len(enc_tokens) - k + 1):
        target_ngram = tuple(enc_tokens[i : i + k])  # build the ngram from the target

        ngram_id = ngram_to_id.get(
            tuple(target_ngram), None
        )  # align the target ngram to the ngrams built from source

        if ngram_id is not None:
            if prev_id is not None and prev_id == ngram_id:
                continue  # Skip duplicate adjacent n-grams
            aln.append(
                {
                    target_ngram: [
                        {"ngram_id": ngram_id, "pos": j}
                        for j in ngram_id_to_pos[ngram_id]
                    ]
                }
            )
            prev_id = ngram_id

    return aln


# def group_ngrams(aln):
#     # group ngram combinations (ensure positions are ordered)
#     position_lists = [list(entry.values())[0] for entry in aln]

#     all_combinations = list(product(*position_lists))
#     grp = []
#     idx = 0
#     for combo in all_combinations:
#         positions = [item["pos"] for item in combo]
#         if positions == sorted(positions):  # Ensure positions are increasing
#             grp.append(list(combo))
#             idx += 1

#     return grp


def group_ngrams(aln):
    position_lists = [list(entry.values())[0] for entry in aln]

    def dfs(idx, path):
        if idx == len(position_lists):
            yield path
            return
        last_pos = path[-1]["pos"] if path else -1
        for candidate in position_lists[idx]:
            if candidate["pos"] > last_pos:
                yield from dfs(idx + 1, path + [candidate])

    grp = list(dfs(0, []))
    return grp


def group_tokens(grp, ngrams):
    # group tokens for each combination of ngrams
    tk_aln = []
    for aln_ngrams in grp:
        pos = aln_ngrams[0]["pos"]
        nid = aln_ngrams[0]["ngram_id"]

        tks = []
        tks += ngrams[pos]["tks"]

        for ng in aln_ngrams[1:]:
            pos = ng["pos"]
            nid = ng["ngram_id"]
            tks += [ngrams[pos]["tks"][-1]]
        tk_aln.append(tks)
    return tk_aln


def build_graph(ngrams, id_to_ngram):
    graph = defaultdict(set)
    for ng in ngrams:
        ngram_id = ng["ngram_id"]
        ngram = id_to_ngram[ngram_id]
        for existing_ngram_id, existing_ngram in id_to_ngram.items():
            if existing_ngram_id == ngram_id:
                continue  # Skip self

            # Check left adjacency (ngram[:-1] matches existing_ngram[1:])
            if ngram[:-1] == existing_ngram[1:]:
                graph[existing_ngram_id].add(ngram_id)

            # Check right adjacency (ngram[1:] matches existing_ngram[:-1])
            if ngram[1:] == existing_ngram[:-1]:
                graph[ngram_id].add(existing_ngram_id)
    return graph


def align_ng(source, target, k=1, verbose=False):
    if verbose:
        print("source", source)
        print("target", target)
        print("-" * 80)
    ngram_to_id, id_to_ngram, ngram_id_to_pos, ngrams = build_index(source, k)
    aln = align_target(target, ngram_to_id, ngram_id_to_pos, k)
    # aln2 = align_target(" " + target.strip(), ngram_to_id, ngram_id_to_pos, k)
    # # max_aln1 = max([len(i) for i in aln1])
    # # max_aln2 = max([len(i) for i in aln2])
    # # print("max_aln1", max_aln1)
    # # print("max_aln2", max_aln2)
    # # aln = aln1 if max_aln1 > max_aln2 else aln2
    if len(aln) > 0:
        grp = group_ngrams(aln)
        tks = group_tokens(grp, ngrams)
        n_aln = len(tks)

        # print(f"{n_aln} alignments")
        return (tks, ngrams, id_to_ngram)
    return ([], ngrams, id_to_ngram)


def reconstruct_target_by_token(source, pos):
    # reconstruct the target by joining the tokens
    return "".join([i["token"] for i in pos])


def reconstruct_target_by_idx(source, pos):
    # reconstruct the target by joining the tokens
    return "".join([source[i["start_idx"] : i["end_idx"]] for i in pos])


# import re
# import tiktoken
# from collections import defaultdict
# import unicodedata


# def norm_text(text):
#     """
#     Normalize text to ensure UTF-8 compatibility for NLP processing.
    
#     This function:
#     1. Normalizes Unicode to the NFC form
#     2. Replaces problematic characters with ASCII equivalents
#     3. Handles common special characters that cause issues
    
#     Args:
#         text (str): Input text to normalize
        
#     Returns:
#         str: Normalized text safe for UTF-8 processing
#     """
#     if not isinstance(text, str):
#         try:
#             text = str(text)
#         except:
#             return ""
    
#     # Step 1: Unicode normalization to NFC form (composed form)
#     # This combines characters and diacritics when possible
#     text = unicodedata.normalize('NFC', text)
    
#     # Step 2: Map specific problematic characters to ASCII equivalents
#     char_map = {
#         'ɛ': 'e',        # epsilon
#         'ɑ': 'a',        # alpha
#         'β': 'b',        # beta
#         'δ': 'd',        # delta
#         'γ': 'g',        # gamma
#         'λ': 'l',        # lambda
#         'μ': 'u',        # mu
#         'π': 'pi',       # pi
#         'θ': 'theta',    # theta
#         'τ': 't',        # tau
#         'ω': 'omega',    # omega
#         '′': "'",        # prime
#         '″': '"',        # double prime
#         '–': '-',        # en dash
#         '—': '--',       # em dash
#         ''': "'",        # curly single quote
#         ''': "'",        # curly single quote
#         '"': '"',        # curly double quote
#         '"': '"',        # curly double quote
#         '…': '...',      # ellipsis
#         '•': '*',        # bullet
#         '·': '.',        # middle dot
#         '×': 'x',        # multiplication sign
#         '÷': '/',        # division sign
#         '≤': '<=',       # less than or equal
#         '≥': '>=',       # greater than or equal
#         '≠': '!=',       # not equal
#         '≈': '~',        # approximately equal
#         '∞': 'inf',      # infinity
#         '∂': 'd',        # partial differential
#         '∫': 'integral', # integral
#         '∑': 'sum',      # sum
#         '∏': 'product',  # product
#         '√': 'sqrt',     # square root
#         '∝': 'prop to',  # proportional to
#         '∠': 'angle',    # angle
#         '△': 'triangle', # triangle
#         '□': 'square',   # square
#         '∈': 'in',       # element of
#         '∉': 'not in',   # not an element of
#         '⊂': 'subset',   # subset
#         '⊃': 'superset', # superset
#         '∪': 'union',    # union
#         '∩': 'intersect',# intersection
#         '⊆': 'subseteq', # subset or equal
#         '⊇': 'superseteq',# superset or equal
#         # Add more mappings as needed
#     }
    
#     for char, replacement in char_map.items():
#         text = text.replace(char, replacement)
#     # Step 3: Remove any remaining non-ASCII characters (optional)
#     # Uncomment if you want to remove ALL non-ASCII characters
#     # text = re.sub(r'[^\x00-\x7F]+', '', text)

#     text.replace("\n", " ")
    
#     return text

# def tokenize_whitespace_with_offsets(text):
#     """Tokenizes text on whitespace and returns tokens with their character start and end positions."""
#     tokens = []

#     for word in re.finditer(r'\S+', text):  # word non-whitespace sequences
#         token = word.group()
#         start_idx = word.start()
#         end_idx = word.end()
        
#         tokens.append({
#             "token": token,
#             "start_idx": start_idx,
#             "end_idx": end_idx
#         })
    
#     return tokens


# def tokenize_with_offsets(text, encoding="cl100k_base"):
#     """Tokenizes text and returns tokens with their character start positions."""
#     enc = tiktoken.get_encoding(encoding)
#     tokens = []

#     etks = enc.encode(text)
#     dtks, ptks = enc.decode_with_offsets(etks)
    
#     assert len(etks) == len(ptks)
    
#     for t, p in zip(etks, ptks):
#         token = enc.decode_single_token_bytes(t).decode("utf-8")
#         tobj = {
#             "token": token,
#             "enc_token": t,
#             "start_idx": p,
#             "end_idx": p + len(token)
#         }
#         tokens.append(tobj)
#     return tokens


# def index_source(source):
#     source_tokens = tokenize_with_offsets(source)
#     tokens = source_tokens

#     source_index = defaultdict(list)
#     for i, token in enumerate(tokens):
#         source_index[token["enc_token"]].append(token)
#     return source_index


# def align_target(target, idx):
#     tokens = tokenize_with_offsets(target)
#     aln = []
#     for token_obj in tokens:
#         enc_token = token_obj["enc_token"]
#         if enc_token in idx.keys():
#             aln.append({enc_token: idx[enc_token]})
#     return aln


# def deduplicate_alignments(aln):
#     pos = []
#     start_idx = 0

#     for d in aln:
#         k, v = next(iter(d.items()))
#         sorted_targets = sorted(v, key=lambda x: x["start_idx"])

#         # Use next with a generator expression to find the first valid match
#         valid_target = next((t for t in sorted_targets if t["start_idx"] >= start_idx), None)

#         if valid_target:
#             start_idx = valid_target["start_idx"]
#             pos.append(valid_target)

#     return pos


# def group_contiguous_tokens(pos):
#     group = []
#     g = []
#     for tk in pos:
#         if len(g) == 0:
#             g.append(tk)
#         elif g[-1]["end_idx"] == tk["start_idx"]:
#             g.append(tk)
#         elif g[-1]["end_idx"] < tk["start_idx"]:
#             group.append({reconstruct_target_by_token("", g): g})
#             g = [tk]
#     group.append({reconstruct_target_by_token("", g): g})
#     return group


# def reconstruct_target_by_token(source, pos):
#     # reconstruct the target by joining the tokens
#     return "".join([i["token"] for i in pos])


# def reconstruct_target_by_idx(source, pos):
#     # reconstruct the target by joining the tokens
#     return "".join([source[i["start_idx"]:i["end_idx"]] for i in pos])


# def reconstruct_target_by_strip_token(source, pos):
#     # reconstruct the target by joining the tokens
#     return " ".join([i["strip_token"] for i in pos])


# def align(source, target):
#     idx = index_source(source)
#     aln = align_target(target, idx)
#     pos = deduplicate_alignments(aln)
#     grp = group_contiguous_tokens(pos)
#     found = reconstruct_target_by_idx(source, pos)
#     return (found, grp)