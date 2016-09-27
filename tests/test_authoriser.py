from nose.tools import assert_equals
import mock, unittest, authoriser
from mock import Mock


class AuthoriserTest(unittest.TestCase):

    @mock.patch('authoriser.urllib2.build_opener', autospec=True)
    def test_auth_with_s3o(self, mock_urllib2):

        code = Mock()
        code.getcode.side_effect = [204, 403]
        resp = Mock()
        resp.open.return_value = code
        mock_urllib2.return_value = resp

        assert_equals(authoriser.auth_with_s3o('123'), True)
        resp.open.assert_called_with('https://s3o.ft.com/token/validate')

        assert_equals(authoriser.auth_with_s3o('123'), False)

    @mock.patch('authoriser.boto3.resource', autospec=True)
    def test_look_up_key_in_dynamo(self, mock_boto3):

        table = Mock()
        resource = Mock()
        resource.Table.return_value = table
        table.get_item.side_effect = [{"Item": {"apiKey": "abc"}}, {"Item": {"apiKey": "abcd"}}]
        mock_boto3.return_value = resource

        assert_equals(authoriser.lookupKeyInDynamo('123', 'abc'), True)
        table.get_item.assert_called_with(AttributesToGet=['apiKey'], Key={'apiId': '123'})

        assert_equals(authoriser.lookupKeyInDynamo('123', 'abc'), False)




