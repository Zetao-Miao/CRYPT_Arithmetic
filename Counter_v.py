from __future__ import annotations
from dataclasses import dataclass, field
from BH import BitHeap


@dataclass
class counter:

    """
    Template for individual GPCs.

    This class tracks:
      - the name of the counter
      - inputs/outputs of the counter
      - cascaded inputs/outputs of the counter
      - which column of the bitheap is this counter applied
    """
    _name: str                                          # name of the counter for human recognition
    _inputs: list[int] = field(default_factory=list)    # inputs of the counter, e.g. [1, 5]
    _outputs: list[int] = field(default_factory=list)   # outputs of the counter, e.g. [1, 1, 1]
    _in_cascade: bool = field(default=False)            # whether this counter is cascaded to another counter via LOOKAHEAD8
    _out_cascade: bool = field(default=False)           # whether this counter can be cascaded to another counter via LOOKAHEAD8
    _applied_column: int = field(default=0)             # which column this counter is applied at
    _LUT_cost: int = field(default=0)


    # ---------- Derived properties (automatically synchronized) ----------
    @property
    def name(self) -> str:
        return self._name

    @property
    def inputs(self) -> list[int]:
        return self._inputs

    @property
    def outputs(self) -> list[int]:
        return self._outputs

    @property
    def in_cascade(self) -> bool:
        return self._in_cascade

    @property
    def out_cascade(self) -> bool:
        return self._out_cascade

    @property
    def applied_column(self) -> int:
        return self._applied_column

    @property
    def LUT_cost(self) -> int:
        return self._LUT_cost

    def __repr__(self):
        return f"counter(name={self._name}, col={self._applied_column})"

    # ---------------------------- Core operations ---------------------------
    def commit(self, bitheap: BitHeap, check_bound=False):
        """commit the counter to the bitheap"""
        if not check_bound:
            # lock input bits in the bitheap
            for i in range(len(self._inputs)):
                bitheap.lock_bits(self.applied_column+i, self._inputs[len(self._inputs) - 1 - i], True if (self._in_cascade and i == 0) else False)
            # add output bits to the next-round list
            for i in range(len(self._outputs)):
                bitheap.add_bits_next_round(self.applied_column+i, self._outputs[len(self._outputs) - 1 - i], True if (self._out_cascade and i == len(self._outputs) - 1) else False)
        else:
            # lock input bits in the bitheap
            for i in range(len(self._inputs)):
                if self.applied_column + i <= bitheap.width - 1:
                    bitheap.lock_bits(self.applied_column+i, self._inputs[len(self._inputs) - 1 - i], True if (self._in_cascade and i == 0) else False)
            for i in range(len(self._outputs)):
                if self.applied_column + i <= bitheap.width - 1:
                    bitheap.add_bits_next_round(self.applied_column+i, self._outputs[len(self._outputs) - 1 - i], True if (self._out_cascade and i == len(self._outputs) - 1) else False)


# -----------------------------------------------------
# list of GPCs used in compressor tree synthesis
# format: (name: str, inputs: list, outputs: list, out_cascade: bool, LUT_cost: int)
# If this list got changed, remember to change get_action_mask_fn correspondingly as well
# -----------------------------------------------------
counter_list = [("(6 : 3]", [6], [1, 1, 1], False, 3),
                ("(3 : 2]", [3], [1, 1], True, 1),
                ("(1,5 : 3]", [1, 5], [1, 1, 1], True, 2),
                ("(2,2,3 : 4]", [2, 2, 3], [1, 1, 1, 1], False, 2),
                ("(9 : 4,1)", [9], [4, 1], False, 3),
                ("(3,9 : 2,3,1)", [3, 9], [2, 3, 1], False, 4),
                ("(4,13 : 3,4,1)", [4, 13], [3, 4, 1], False, 6),
                ("(5,17 : 4,5,1)", [5, 17], [4, 5, 1], False, 8)]