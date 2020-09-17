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
Unit tests for the :mod:`pennylane.devices.DefaultMixed` device.
"""

import pytest
import pennylane as qml
from pennylane.ops import PauliZ, CZ, PauliX, Hadamard, CNOT, AmplitudeDamping, DepolarizingChannel
from pennylane.devices.default_mixed import DefaultMixed
import numpy as np

INV_SQRT2 = 1 / np.sqrt(2)

diags = [PauliZ, CZ, PauliX]
gates = [PauliX, Hadamard, CNOT]
channels = [AmplitudeDamping, DepolarizingChannel]

@pytest.mark.parametrize("nr_wires", [1, 2, 3])
class TestCreateBasisState:
    """Unit tests for the method `_create_basis_state()`"""

    def test_shape(self, nr_wires):
        """Tests that the basis state has the correct shape"""
        dev = qml.device('default.mixed', wires=nr_wires)

        assert [2] * (2 * nr_wires) == list(np.shape(dev._create_basis_state(0)))

    @pytest.mark.parametrize("index", [0, 1])
    def test_expected_state(self, nr_wires, index):
        """Tests output basis state against the expected one"""
        rho = np.zeros((2 ** nr_wires, 2 ** nr_wires))
        rho[index, index] = 1
        rho = np.reshape(rho, [2] * (2 * nr_wires))
        dev = qml.device('default.mixed', wires=nr_wires)

        assert np.allclose(rho, dev._create_basis_state(index))


@pytest.mark.parametrize("nr_wires", [1, 2, 3])
class TestState:
    """Tests for the method `state()`, which retrieves the state of the system"""
    # Note: These tests need to be extended once we can output non-basis states

    def test_shape(self, nr_wires):
        """Tests that the state has the correct shape"""
        dev = qml.device('default.mixed', wires=nr_wires)

        assert (2 ** nr_wires, 2 ** nr_wires) == np.shape(dev.state)

    def test_init_state(self, nr_wires):
        """Tests that the state is |0...0><0...0| after initialization of the device"""
        rho = np.zeros((2 ** nr_wires, 2 ** nr_wires))
        rho[0, 0] = 1
        dev = qml.device('default.mixed', wires=nr_wires)

        assert np.allclose(rho, dev.state)


@pytest.mark.parametrize("nr_wires", [1, 2, 3])
class TestReset:
    """Unit tests for the method `reset()`"""

    def test_reset_basis_state(self, nr_wires):
        assert 1 == 1


@pytest.mark.parametrize("nr_wires", [1, 2, 3])
class TestAnalyticProb:
    """Unit tests for the method `analytic_probability()` """

    # Note: more tests required for other states
    def test_prob_init_states(self, nr_wires):
        """Tests that we obtain the correct probabilities for the state |0...0><0...0|"""
        dev = qml.device('default.mixed', wires=nr_wires)
        probs = np.zeros(2 ** nr_wires)
        probs[0] = 1

        assert np.allclose(probs, dev.analytic_probability())


class TestKrausOps:
    """Unit tests for the method `_get_kraus_ops()`"""

    @pytest.mark.parametrize("ops", unitary_ops)
    def test_unitary_kraus(self, ops):
        """Tests that matrices of non-diagonal unitary operations are retrieved correctly"""
        dev = qml.device('default.mixed', wires=2)

        assert np.allclose(dev._get_kraus(ops[0]), [ops[1]])

    @pytest.mark.parametrize("ops", diagonal_ops)
    def test_diagonal_kraus(self, ops):
        """Tests that matrices of non-diagonal unitary operations are retrieved correctly"""
        dev = qml.device('default.mixed', wires=2)
        assert np.allclose(dev._get_kraus(ops[0]), ops[1])

    @pytest.mark.parametrize("ops", channel_ops)
    def test_channel_kraus(self, ops):
        """Tests that krause matrices of non-unitary channels are retrieved correctly"""
        dev = qml.device('default.mixed', wires=1)

        assert np.allclose(dev._get_kraus(ops[0]), ops[1])


class TestApplyChannel:
    """Unit tests for the method `_apply_channel()`"""


class TestApplyDiagonal:
    """Unit tests for the method `_apply_diagonal_unitary()`"""


class TestApplyOperation:
    """Unit tests for the method `_apply_operation()`"""


class TestApply:
    """Unit tests for the main method `apply()`"""
