from read_uncommited import dirty_read
from read_commited import non_repeatable_reads
from repeatable_read import phantom_reads
from serializable import serializable
from deadlock import deadlock


if __name__ == "__main__":
    # dirty_read()
    # non_repeatable_reads()
    phantom_reads()
    # serializable()
    # deadlock()
