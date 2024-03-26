# test_generate_embedding.py

import pytest
from pydantic import ValidationError
from app.utils.embeddings import generate_embedding, EmbeddingRequest, EmbeddingResponse
from openai.types import CreateEmbeddingResponse


@pytest.fixture
def mock_openai_client(mocker):
    """
    A pytest fixture that uses the pytest-mock plugin to mock the OpenAI client,
    configured to handle both single and multiple text inputs.
    """

    def create_response(input, model):
        # Simulate a different response based on the input type (single vs list)
        if isinstance(input, list):
            data = [
                {
                    "object": "embedding",
                    "index": idx,
                    "embedding": [0.1 * idx, 0.2, 0.3],
                }
                for idx, _ in enumerate(input)
            ]
        else:
            data = [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]}]

        return CreateEmbeddingResponse(
            object="list",
            model=model,
            usage={"prompt_tokens": 5, "total_tokens": 5},
            data=data,
        )

    mock_client = mocker.Mock()
    mock_client.embeddings.create.side_effect = create_response
    return mock_client


def test_generate_embedding_multiple_texts(mock_openai_client):
    """
    Test the generate_embedding function with multiple pieces of text.
    """
    texts = ["first text", "second text"]
    request = EmbeddingRequest(text=texts, model="text-embedding-model")
    response = generate_embedding(request, mock_openai_client)

    assert isinstance(
        response, EmbeddingResponse
    ), "Response should be an instance of EmbeddingResponse"
    assert len(response.embeddings) == len(
        texts
    ), "There should be an embedding for each text"

    for idx, embedding in enumerate(response.embeddings):
        assert (
            embedding.index == idx
        ), f"The embedding index {idx} should match the mock response"
        assert embedding.embedding == [
            0.1 * idx,
            0.2,
            0.3,
        ], f"The embedding vector for index {idx} should match the mock response"
        assert (
            embedding.object == "embedding"
        ), "The object attribute should be 'embedding'"


def test_generate_embedding_single_text(mock_openai_client):
    """
    Test the generate_embedding function with a single piece of text.
    """
    request = EmbeddingRequest(text="test text", model="text-embedding-model")
    response = generate_embedding(request, mock_openai_client)

    assert isinstance(
        response, EmbeddingResponse
    ), "Response should be an instance of EmbeddingResponse"
    assert (
        len(response.embeddings) == 1
    ), "There should be one embedding in the response"
    embedding = response.embeddings[0]
    assert embedding.index == 0, "The embedding index should match the mock response"
    assert embedding.embedding == [
        0.1,
        0.2,
        0.3,
    ], "The embedding vector should match the mock response"
    assert embedding.object == "embedding", "The object attribute should be 'embedding'"


def test_generate_embedding_validation_error():
    """
    Test the generate_embedding function with invalid inputs to ensure validation errors are raised.
    """
    # Passing the wrong type for the text field
    with pytest.raises(ValidationError):
        request = EmbeddingRequest(
            text={"wrong": "type"},
            model="somemodel",
        )
