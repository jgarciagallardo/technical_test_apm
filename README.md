# APMC technical test
### Technical choice 

Two of the most popular framework to test API rest are Pytest and Postman

While Postman offers a user-friendly interface and is a great tool for initial API exploration and simple testing, I've opted for Pytest for my API validation needs. Here's why:

**Scalability and Automation:** As my testing suite grows in size and complexity, Pytest's framework provides a robust foundation for creating highly maintainable and automated tests. With features like fixtures, parametrization, and plugins, I can easily organize and execute a large number of tests efficiently. Postman, while capable of automation, may become limiting when dealing with intricate test scenarios and complex data structures.

**Flexibility:** Pytest offers unparalleled flexibility through Python's extensive ecosystem of libraries and tools. This enables me to customize my tests to meet specific requirements, integrate with other testing frameworks, and leverage advanced testing techniques. Postman, while offering a rich feature set, is primarily designed for API testing and may not provide the same level of customization as a general-purpose testing framework like Pytest.

**Integration with CI/CD:** Pytest seamlessly integrates into CI/CD pipelines, allowing for continuous testing and ensuring code quality. This enables me to catch issues early in the development process and deliver more reliable software. While Postman can also be integrated into CI/CD pipelines, Pytest's command-line interface and flexibility make it a more natural fit for automated testing environments.

**Advanced Testing Features:** Pytest supports a wide range of testing features, including mocking, patching, and test-driven development (TDD), which can be invaluable for writing comprehensive and reliable tests. Postman, while offering some testing capabilities, may not be as well-suited for these advanced testing techniques.
In summary, while Postman is an excellent tool for initial API exploration and simple testing, Pytest's scalability, flexibility, and integration with the broader Python ecosystem make it a more compelling choice for comprehensive API validation. By leveraging Pytest's capabilities, I can create a robust and maintainable testing suite that ensures the quality of my API and supports ongoing development efforts."

### How to run the test

+ Clone the repository


+ Add a valid token with access to user information to <code>github_token</code> in <code>src/config.json</code>


+ Add a valid token without any access to <code>gitgithub_token_forbiddenhub_token</code> in <code>src/config.json</code>
    

+ Install python3 if not yet installed.


+ Install virtual environment package.


    pip install venv

+ Create virtual environment.


    virtualenv venv 

+ Activate virtual environment.


    venv\Scripts\activate

+ Install required packages.


    pip install -r requirements.txt



+ Run test from <code>src</code> folder.

    
    pytest task1.py
    pytest task2.py
    pytest task3.py
    pytest task4.py
    pytest task5.py
    pytest task6.py
    pytest task7.py