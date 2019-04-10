import logging, sys, argparse


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_entity(tag_seq, char_seq):
    STY = get_STY_entity(tag_seq, char_seq)
    LOC = get_LOC_entity(tag_seq, char_seq)
    TYP = get_TYP_entity(tag_seq, char_seq)
    return STY, LOC, TYP


def get_STY_entity(tag_seq, char_seq):
    length = len(char_seq)
    STY = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-STY':
            if 'per' in locals().keys():
                STY.append(per)
                del per
            per = char
            if i+1 == length:
                STY.append(per)
        if tag == 'I-STY':
            per += char
            if i+1 == length:
                STY.append(per)
        if tag not in ['I-STY', 'B-STY']:
            if 'per' in locals().keys():
                STY.append(per)
                del per
            continue
    return STY


def get_LOC_entity(tag_seq, char_seq):
    length = len(char_seq)
    LOC = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == length:
                LOC.append(loc)
        if tag == 'I-LOC':
            loc += char
            if i+1 == length:
                LOC.append(loc)
        if tag not in ['I-LOC', 'B-LOC']:
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue
    return LOC


def get_TYP_entity(tag_seq, char_seq):
    length = len(char_seq)
    TYP = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-TYP':
            if 'org' in locals().keys():
                TYP.append(org)
                del org
            org = char
            if i+1 == length:
                TYP.append(org)
        if tag == 'I-TYP':
            org += char
            if i+1 == length:
                TYP.append(org)
        if tag not in ['I-TYP', 'B-TYP']:
            if 'org' in locals().keys():
                TYP.append(org)
                del org
            continue
    return TYP


def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
