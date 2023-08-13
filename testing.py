# sourcery skip: dont-import-test-modules
from tests.test_anthropic_chat import test_anthropic_chat
# sourcery skip: dont-import-test-modules
from tests.test_openai_image import test_openai_image
# sourcery skip: dont-import-test-modules
from tests.test_openai_chat import test_openai_chat
# sourcery skip: dont-import-test-modules
from tests.test_chroma_db import testing_vectorstore
# sourcery skip: dont-import-test-modules
from tests.test_openai_messages import test_openai_messages
# sourcery skip: dont-import-test-modules
from tests.test_context_window import test_context_window

def run_test_suite():
    testing_vectorstore()
    test_openai_image()
    test_openai_chat()
    test_anthropic_chat()
    test_openai_messages()
    test_context_window()

if __name__ == "__main__":
    run_test_suite()