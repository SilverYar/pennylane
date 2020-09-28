# Copyright 2018-2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module contains the CircuitGraph class which is used to generate a DAG (directed acyclic graph)
representation of a quantum circuit from an operator and observable queue.
"""
import networkx as nx

from pennylane.circuit_graph import CircuitGraph, Layer, LayerData


class TapeCircuitGraph(CircuitGraph):
    """New circuit graph object. This will eventually grow to replace
    the existing CircuitGraph; for now, we simply inherit from the
    current CircuitGraph, and modify the instantiation so that it
    can be created via the quantum tape."""

    def __init__(self, ops, obs, wires, par_info=None, trainable_params=None):
        self._operations = ops
        self._observables = obs
        self.par_info = par_info
        self.trainable_params = trainable_params
        super().__init__(ops + obs, variable_deps={}, wires=wires)

    @property
    def operations(self):
        """Operations in the circuit."""
        return self._operations

    @property
    def observables(self):
        """Observables in the circuit."""
        return self._observables

    def has_path(self, a, b):
        """Checks if a path exists between the two given nodes.

        Args:
            a (Operator): initial node
            b (Operator): final node

        Returns:
            bool: returns ``True`` if a path exists
        """
        return nx.has_path(self._graph, a, b)

    @property
    def parametrized_layers(self):
        """Identify the parametrized layer structure of the circuit.

        Returns:
            list[Layer]: layers of the circuit
        """
        # FIXME maybe layering should be greedier, for example [a0 b0 c1 d1] should layer as [a0
        # c1], [b0, d1] and not [a0], [b0 c1], [d1] keep track of the current layer
        current = Layer([], [])
        layers = [current]

        # sort vars by first occurrence of the var in the ops queue
        variable_ops_sorted = []

        for idx, info in self.par_info.items():
            if idx in self.trainable_params:
                op = info["op"]

                # get all predecessor ops of the op
                sub = self.ancestors((op,))

                # check if any of the dependents are in the
                # currently assembled layer
                if set(current.ops) & sub:
                    # operator depends on current layer, start a new layer
                    current = Layer([], [])
                    layers.append(current)

                # store the parameters and ops indices for the layer
                current.ops.append(op)
                current.param_inds.append(idx)

        return layers