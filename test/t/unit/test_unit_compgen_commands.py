import pytest

from conftest import assert_bash_exec, bash_env_saved


@pytest.mark.bashcomp(cmd=None, ignore_env=r"^\+COMPREPLY=")
class TestUtilCompgenCommands:
    @pytest.fixture(scope="class")
    def functions(self, request, bash):
        assert_bash_exec(
            bash,
            r"_comp_compgen_commands__test() {"
            r"    local COMPREPLY=() cur=${1-};"
            r"    _comp_compgen_commands;"
            r'    printf "%s\n" "${COMPREPLY[@]}";'
            r"}",
        )

    def test_basic(self, bash, functions):
        output = assert_bash_exec(
            bash, "_comp_compgen_commands__test sh", want_output=True
        )
        assert output.strip()

    @pytest.mark.parametrize(
        "shopt_no_empty,result_empty", ((True, True), (False, False))
    )
    def test_empty(self, bash, functions, shopt_no_empty, result_empty):
        with bash_env_saved(bash) as bash_env:
            bash_env.shopt("no_empty_cmd_completion", shopt_no_empty)
            output = assert_bash_exec(
                bash, "_comp_compgen_commands__test", want_output=True
            )
        assert (output.strip() == "") == result_empty
