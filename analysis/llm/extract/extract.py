import re
import tiktoken
from collections import defaultdict


def clean_text(text):
    # strip leading/trailing whitespace
    text = text.strip()
    # remove newlines
    text = text.replace("\n", " ")
    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize_whitespace_with_offsets(text):
    """Tokenizes text on whitespace and returns tokens with their character start and end positions."""
    tokens = []

    for word in re.finditer(r'\S+', text):  # word non-whitespace sequences
        token = word.group()
        start_idx = word.start()
        end_idx = word.end()
        
        tokens.append({
            "token": token,
            "start_idx": start_idx,
            "end_idx": end_idx
        })
    
    return tokens


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
            "end_idx": p + len(token)
        }
        tokens.append(tobj)
    return tokens


def index_source(source):
    source_tokens = tokenize_with_offsets(source)
    tokens = source_tokens

    source_index = defaultdict(list)
    for i, token in enumerate(tokens):
        source_index[token["enc_token"]].append(token)
    return source_index


def align_target(target, idx):
    tokens = tokenize_with_offsets(target)
    aln = []
    for token_obj in tokens:
        enc_token = token_obj["enc_token"]
        if enc_token in idx.keys():
            aln.append({enc_token: idx[enc_token]})
    return aln


def deduplicate_alignments(aln):
    pos = []
    start_idx = 0

    for d in aln:
        k, v = next(iter(d.items()))
        sorted_targets = sorted(v, key=lambda x: x["start_idx"])

        # Use next with a generator expression to find the first valid match
        valid_target = next((t for t in sorted_targets if t["start_idx"] >= start_idx), None)

        if valid_target:
            start_idx = valid_target["start_idx"]
            pos.append(valid_target)

    return pos


def group_contiguous_tokens(pos):
    group = []
    g = []
    for tk in pos:
        if len(g) == 0:
            g.append(tk)
        elif g[-1]["end_idx"] == tk["start_idx"]:
            g.append(tk)
        elif g[-1]["end_idx"] < tk["start_idx"]:
            group.append({reconstruct_target_by_token("", g): g})
            g = [tk]
    group.append({reconstruct_target_by_token("", g): g})
    return group


def reconstruct_target_by_token(source, pos):
    # reconstruct the target by joining the tokens
    return "".join([i["token"] for i in pos])


def reconstruct_target_by_idx(source, pos):
    # reconstruct the target by joining the tokens
    return "".join([source[i["start_idx"]:i["end_idx"]] for i in pos])


def reconstruct_target_by_strip_token(source, pos):
    # reconstruct the target by joining the tokens
    return " ".join([i["strip_token"] for i in pos])


def align(source, target):
    idx = index_source(source)
    aln = align_target(target, idx)
    pos = deduplicate_alignments(aln)
    grp = group_contiguous_tokens(pos)
    found = reconstruct_target_by_idx(source, pos)
    return (found, grp)