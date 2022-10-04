class Tester():
    def __init__(self) -> None:
        self.tests = []

    def test(self, testname: str, *, erro: bool = False):
        def add_test(test):
            self.tests.append({
                'name': testname,
                'test': test,
                'erro': erro,
            })

            return test

        return add_test

    def run_tests(self):
        for test in self.tests:
            try:
                test['test']()

                if test['erro']:
                    print('TEST ' + test['name'] + ' FAILED (should have errored)')
                else:
                    print('TEST ' + test['name'] + ' PASSED')
            except Exception as e:
                if test['erro']:
                    print('TEST ' + test['name'] + ' PASSED (errored)')
                else:
                    print(f'\nTEST ' + test['name'] + ' FAILED')
                    print(e)
                    print('\n')
