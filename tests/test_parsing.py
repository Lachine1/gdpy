from gdpy.utils.parsing import parse_list_response, parse_response


class TestParsing:
    def test_parse_response(self):
        response = "1:username:2:12345:3:100"
        result = parse_response(response)
        assert result == {"1": "username", "2": "12345", "3": "100"}

    def test_parse_response_with_pipe(self):
        response = "1:value1:2:value2|3:value3:4:value4"
        result = parse_response(response)
        assert result == {"1": "value1", "2": "value2", "3": "value3", "4": "value4"}

    def test_parse_response_error(self):
        result = parse_response("-1")
        assert result == {"_error": -1}

        result = parse_response("-11")
        assert result == {"_error": -11}

    def test_parse_list_response(self):
        response = "1:name1:2:id1|1:name2:2:id2"
        result = parse_list_response(response)
        assert len(result) == 2
        assert result[0] == {"1": "name1", "2": "id1"}
        assert result[1] == {"1": "name2", "2": "id2"}

    def test_parse_list_response_empty(self):
        result = parse_list_response("-1")
        assert result == []
