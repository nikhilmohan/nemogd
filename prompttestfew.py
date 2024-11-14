from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.pydantic_v1 import BaseModel, Field


import json

from langchain.output_parsers import PydanticOutputParser

class Summary(BaseModel):
    subject: str = Field(description="The central concept about which the query is asked. Should be one of site, node, alarm, ticket")
    references: list[str] = Field(description="The additional concepts which provide context to the central concept in the query. Choose only if present in the query. Should use only the following terms: Site, Node, Alarm, Ticket.")
    keywords: list[str] = Field(description="Important words that describe the query. Choose only those words that are actually present in the query.")
    identifier: str = Field(description="Identifier for the central concept if present in the query, blank if none is present")

pydantic_parser = PydanticOutputParser(pydantic_object=Summary)
format_instructions = pydantic_parser.get_format_instructions()

information = """
Following are the four key network operations related concepts associated with your telecom company - Site, Node, Alarm, Ticket
A 'site' refers to the physical location at which multiple nodes belonging to your network are located.
A 'site' can have many devices or nodes and is identified by a 'site id' that has a prefix of 'abc'.
Site related questions can be generic network wide or about a specific site that is identified using a 'site id'
A 'device' may also be referred to as a 'node'.
A device performs a networking function.
The 'device' or 'node' will have lots of performance indicator attributes that can be monitored such as 'bandwidth' 
to detect any anomalies or unusual behaviour in the network.
A 'device' is identified by a 'device id'. 
The 'device' or 'node' may also raise 'alarms' when an unusual event occurs. 
'bad-link-detected', 'lagdown' are some example alarms reported in devices of 'OLT' type.
Node related questions can be generic network wide or about nodes located in a specific site using site id or about a specific node that is identified using a 'node id'
An 'alarm' is identified by an 'alarm id'
A 'ticket' refers to an incident that is reported in the ticket management system to manage network operations issues. 
A 'ticket' is identified by a 'ticket id' and is normally associated with an 'alarm'
"""

template = """You are an experienced network operations engineer in a telecom company. Analyse the questions asked by the users that are 
     related to operations of your network. Your job is to extract key information from the question in the format {format_instructions}.
     Refer to the following information as guidance to understand the details of the network that you are managing. 
     {information}
     The answer should have only words that are present in the query. If the question is unrelated to network operations or you are not able to answer, politely refuse to answer the question
     
    question: {input}
    {answer}
    """

examples = [
    {
        """
        You are an experienced network operations engineer in a telecom company. Analyse the questions asked by the users that are 
     related to operations of your network. Your job is to extract key information from the question in the format The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"subject": {"title": "Subject", "description": "The central concept about which the query is asked. Should be one of site, node, alarm, ticket", "type": "string"}, "references": {"title": "References", "description": "The additional concepts which provide context to the central concept in the query. Choose only if present in the query. Should use only the following terms: Site, Node, Alarm, Ticket.", "type": "array", "items": {"type": "string"}}, "keywords": {"title": "Keywords", "description": "Important words that describe the query. Choose only those words that are actually present in the query.", "type": "array", "items": {"type": "string"}}, "identifier": {"title": "Identifier", "description": "Identifier for the central concept if present in the query, blank if none is present", "type": "string"}}, "required": ["subject", "references", "keywords", "identifier"]}
```.
     Refer to the following information as guidance to understand the details of the network that you are managing. 
     
Following are the four key network operations related concepts associated with your telecom company - Site, Node, Alarm, Ticket
A 'site' refers to the physical location at which multiple nodes belonging to your network are located.
A 'site' can have many devices or nodes and is identified by a 'site id' that has a prefix of 'abc'.
Site related questions can be generic network wide or about a specific site that is identified using a 'site id'
A 'device' may also be referred to as a 'node'.
A device performs a networking function.
The 'device' or 'node' will have lots of performance indicator attributes that can be monitored such as 'bandwidth' 
to detect any anomalies or unusual behaviour in the network.
A 'device' is identified by a 'device id'. 
The 'device' or 'node' may also raise 'alarms' when an unusual event occurs. 
'bad-link-detected', 'lagdown' are some example alarms reported in devices of 'OLT' type.
Node related questions can be generic network wide or about nodes located in a specific site using site id or about a specific node that is identified using a 'node id'
An 'alarm' is identified by an 'alarm id'
A 'ticket' refers to an incident that is reported in the ticket management system to manage network operations issues. 
A 'ticket' is identified by a 'ticket id' and is normally associated with an 'alarm'

     The answer should have only words that are present in the query. If the question is unrelated to network operations or you are not able to answer, politely refuse to answer the question
     
    question: What is the most problematic site?
    subject='site' references=[] keywords=['problematic'] identifier=''
    """
    },
     {
        """
        You are an experienced network operations engineer in a telecom company. Analyse the questions asked by the users that are 
     related to operations of your network. Your job is to extract key information from the question in the format The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"subject": {"title": "Subject", "description": "The central concept about which the query is asked. Should be one of site, node, alarm, ticket", "type": "string"}, "references": {"title": "References", "description": "The additional concepts which provide context to the central concept in the query. Choose only if present in the query. Should use only the following terms: Site, Node, Alarm, Ticket.", "type": "array", "items": {"type": "string"}}, "keywords": {"title": "Keywords", "description": "Important words that describe the query. Choose only those words that are actually present in the query.", "type": "array", "items": {"type": "string"}}, "identifier": {"title": "Identifier", "description": "Identifier for the central concept if present in the query, blank if none is present", "type": "string"}}, "required": ["subject", "references", "keywords", "identifier"]}
```.
     Refer to the following information as guidance to understand the details of the network that you are managing. 
     
Following are the four key network operations related concepts associated with your telecom company - Site, Node, Alarm, Ticket
A 'site' refers to the physical location at which multiple nodes belonging to your network are located.
A 'site' can have many devices or nodes and is identified by a 'site id' that has a prefix of 'abc'.
Site related questions can be generic network wide or about a specific site that is identified using a 'site id'
A 'device' may also be referred to as a 'node'.
A device performs a networking function.
The 'device' or 'node' will have lots of performance indicator attributes that can be monitored such as 'bandwidth' 
to detect any anomalies or unusual behaviour in the network.
A 'device' is identified by a 'device id'. 
The 'device' or 'node' may also raise 'alarms' when an unusual event occurs. 
'bad-link-detected', 'lagdown' are some example alarms reported in devices of 'OLT' type.
Node related questions can be generic network wide or about nodes located in a specific site using site id or about a specific node that is identified using a 'node id'
An 'alarm' is identified by an 'alarm id'
A 'ticket' refers to an incident that is reported in the ticket management system to manage network operations issues. 
A 'ticket' is identified by a 'ticket id' and is normally associated with an 'alarm'

     The answer should have only words that are present in the query. If the question is unrelated to network operations or you are not able to answer, politely refuse to answer the question
     
    question: What are the top most occuring alarms?
    subject='alarm' references=[] keywords=['top', 'occuring'] identifier=''
    """
    },
    {
        """
        You are an experienced network operations engineer in a telecom company. Analyse the questions asked by the users that are 
     related to operations of your network. Your job is to extract key information from the question in the format The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"subject": {"title": "Subject", "description": "The central concept about which the query is asked. Should be one of site, node, alarm, ticket", "type": "string"}, "references": {"title": "References", "description": "The additional concepts which provide context to the central concept in the query. Choose only if present in the query. Should use only the following terms: Site, Node, Alarm, Ticket.", "type": "array", "items": {"type": "string"}}, "keywords": {"title": "Keywords", "description": "Important words that describe the query. Choose only those words that are actually present in the query.", "type": "array", "items": {"type": "string"}}, "identifier": {"title": "Identifier", "description": "Identifier for the central concept if present in the query, blank if none is present", "type": "string"}}, "required": ["subject", "references", "keywords", "identifier"]}
```.
     Refer to the following information as guidance to understand the details of the network that you are managing. 
     
Following are the four key network operations related concepts associated with your telecom company - Site, Node, Alarm, Ticket
A 'site' refers to the physical location at which multiple nodes belonging to your network are located.
A 'site' can have many devices or nodes and is identified by a 'site id' that has a prefix of 'abc'.
Site related questions can be generic network wide or about a specific site that is identified using a 'site id'
A 'device' may also be referred to as a 'node'.
A device performs a networking function.
The 'device' or 'node' will have lots of performance indicator attributes that can be monitored such as 'bandwidth' 
to detect any anomalies or unusual behaviour in the network.
A 'device' is identified by a 'device id'. 
The 'device' or 'node' may also raise 'alarms' when an unusual event occurs. 
'bad-link-detected', 'lagdown' are some example alarms reported in devices of 'OLT' type.
Node related questions can be generic network wide or about nodes located in a specific site using site id or about a specific node that is identified using a 'node id'
An 'alarm' is identified by an 'alarm id'
A 'ticket' refers to an incident that is reported in the ticket management system to manage network operations issues. 
A 'ticket' is identified by a 'ticket id' and is normally associated with an 'alarm'

     The answer should have only words that are present in the query. If the question is unrelated to network operations or you are not able to answer, politely refuse to answer the question
     
    question: What is the most problematic node?
    subject='node' references=[] keywords=['problematic'] identifier=''
    """
    },
     {
        """
        You are an experienced network operations engineer in a telecom company. Analyse the questions asked by the users that are 
     related to operations of your network. Your job is to extract key information from the question in the format The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"subject": {"title": "Subject", "description": "The central concept about which the query is asked. Should be one of site, node, alarm, ticket", "type": "string"}, "references": {"title": "References", "description": "The additional concepts which provide context to the central concept in the query. Choose only if present in the query. Should use only the following terms: Site, Node, Alarm, Ticket.", "type": "array", "items": {"type": "string"}}, "keywords": {"title": "Keywords", "description": "Important words that describe the query. Choose only those words that are actually present in the query.", "type": "array", "items": {"type": "string"}}, "identifier": {"title": "Identifier", "description": "Identifier for the central concept if present in the query, blank if none is present", "type": "string"}}, "required": ["subject", "references", "keywords", "identifier"]}
```.
     Refer to the following information as guidance to understand the details of the network that you are managing. 
     
Following are the four key network operations related concepts associated with your telecom company - Site, Node, Alarm, Ticket
A 'site' refers to the physical location at which multiple nodes belonging to your network are located.
A 'site' can have many devices or nodes and is identified by a 'site id' that has a prefix of 'abc'.
Site related questions can be generic network wide or about a specific site that is identified using a 'site id'
A 'device' may also be referred to as a 'node'.
A device performs a networking function.
The 'device' or 'node' will have lots of performance indicator attributes that can be monitored such as 'bandwidth' 
to detect any anomalies or unusual behaviour in the network.
A 'device' is identified by a 'device id'. 
The 'device' or 'node' may also raise 'alarms' when an unusual event occurs. 
'bad-link-detected', 'lagdown' are some example alarms reported in devices of 'OLT' type.
Node related questions can be generic network wide or about nodes located in a specific site using site id or about a specific node that is identified using a 'node id'
An 'alarm' is identified by an 'alarm id'
A 'ticket' refers to an incident that is reported in the ticket management system to manage network operations issues. 
A 'ticket' is identified by a 'ticket id' and is normally associated with an 'alarm'

     The answer should have only words that are present in the query. If the question is unrelated to network operations or you are not able to answer, politely refuse to answer the question
     
    question: What are the recently identified correlations in the site abc-123??
    subject='alarm' references=['Site'] keywords=['recently', 'identified', 'correlations'] identifier='abc-123'
    """
    }
]
example_prompt = PromptTemplate(template=template, 
                        input_variables=["input", "information"],
                        partial_variables={"format_instructions": pydantic_parser.get_format_instructions()})

query = "What is the most problematic site?"
# print(example_prompt.format(examples[0]))

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="question: {input}",
    input_variables=["input"],
)

print(prompt.format(input=query))

llm = OllamaLLM(model="llama3", temperature=0)

chain = prompt | llm | pydantic_parser



query_list = [
              "What is the most problematic site?",
              "What are the recently identified correlations?",
              "What are the top most affected sites?",
              "What is the most problematic node?",
              "What are the top affected nodes?",
              "Any anomalies detected?",
              "What are the top most occuring alarms?",
              "What are the recently identified correlations in the site abc-123?"
              
]
for query in query_list:
    result = chain.invoke({"input": query, "information": information})
    print("query: " + query)
    print("answer")
    print(result)
    print("****")

