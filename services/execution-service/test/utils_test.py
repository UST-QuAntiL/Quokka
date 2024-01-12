from qiskit_ibm_provider import IBMProvider

def get_available_qpu(credentials):
    provider = IBMProvider(**credentials)
    backends = provider.backends()
    for backend in backends:
        if 'simulator' not in backend.name:
            return backend.name