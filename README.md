# client command line tool


When testing the command line tool functionality, please run the server on port `32768` as I assumed the service url should be fixed and therefore each client should have a their own base url.


# How to build client command line tool
1. Download the zip file
2. Extract the zip file
3. Open the extracted folder
4. Run `python setup.py install` or ``python3 setup.py install` to install the client command line tool
5. Run `cpx -h` to confirm whether it has been installed successfully. The help documentation should be shown, if cpx client command line tool is installed.


# How to use client command line tool
You can use `cpx [-h] [-n N] [--data DATA] [--service SERVICE] [--timeout TIMEOUT] operator target` to interact with cpx server

Required arguments:
  `operator`           the option to select which operation to do to the target [options: get, watch]
  `target`             the target to interact [options: services, average]

Optional arguments:
  `-n N`               the update rate for watch operation e.g. `cpx watch services`
  `--data DATA`        the data you would to like to get its average `cpx get average` (default: None)
  `--service SERVICE`  the service name you would to like to get its status `cpx get services` or average `cpx get average` (default: None)
  `--timeout TIMEOUT`  the request timeout limit (default: 60s)

For now, there are 5 usages in total:
1. `cpx get services`                                Get the statuses of all services' instances on cpx server
2. `cpx get services --service SERVICE`              Get the statuses of all instances of a specific service on cpx server
3. `cpx get average --data DATA --service SERVICE`   Get the average of a specific data from a specfic service on cpx server
4. `cpx watch services`                              Watch the statuses of all services' instances on cpx server continuously
5. `cpx watch services --service SERVICE`            Watch the statuses of all instances of a specific service on cpx server continuously


# How to run unit tests
1. use `pip install -r test-requirements.txt` to install all test dependencies
2. use `pytest`


# User experience design considerations:
For command line tool, I think the followings points are quite important:
1. Easy to install
2. Easy to use
3. As out-of-the-box as possible (Less dependencies)
4. Fast performance

I would explain what kind of decisions and trade-offs regarding to each point. 
After that, I would explain what kind of future improvement could be done.

1. Command line tool is often used as a tool to handle repetitive and operational tasks. 
   It's not expected to take a lot of time to install/configure to use it. 
   The optimal case is to use bash to create this kind of tool so that the user can just download it and start using it.
   However, some complex logics might not be easy to develop in bash (e.g. handling requests asynchronously) 
   and it might not be worth it to develop it from scratch just for building this tool.

   Therefore, I chose Python so that we could speed up development of this tool. 
   After all, the user can also easily install it through pip and it's not affecting the user experience very much,
   but we could greatly increase development speed and I think the trade-off is worth it.

2. As I mentioned, Command line tool is used daily. Steep learning curve should be avoided.
   I try to use more plain English or familiar command (e.g. -n in watch) in the command usage.
   So that the user can get the idea of these commands and start to use it as quickly as possible.

3. The tool should be stable enough as the user would use it daily. The more dependencies we add, the more likely we break the tool.
   Here I tried to use as less dependencies as possible. However, I don't think it is worth spending too much time on developing 
   asynchronous request handling and data validation from scratch, as it's not point of the tool. I made a trade-off here to make
   python, aiohttp and pydantic as the dependencies here for development speed. 
   Python is well-known for fast development because of its flexibility, but on the other hand, this advantage also makes it prone to errors.
   In order to compensate the weakness of using python, I cover most of the use cases in tests. 
   Also, I used pydantic to do data validation, which could validate the data type and make us easier to catch data type related bugs.
   With these compensations, I think the trade-off is acceptable.

4. This tool is IO bound and therefore I used asynchronous requests to resolve the blocking IO issue. 
   Without the blocking IO issue, the tool can retrieve the instance status on each ip address almost in parallel, improving the performance greatly.
   In order to handle requests asynchronously, I used aiohttp, which is a trade-off to sacrifice less dependencies to improve performance,
   but it's definitely worth it.


# Code quality design considerations:
There are also some design considerations to talk about regarding to the code quality.
1. I have developed BaseClient in client.py, which could be used for inheritance and make us easier to develop new type of client, as it already contains
   some of the most important basic functionalities that are needed for other possible clients. If it doesn't include some server specific features,
   we could always extend it in the new client class.

2. I put dependency injection conception on focus in this tool. Therefore, I have separated the code structure into several layers:
    request layer, client layer, model layer, command line tool function layer, command line tool layer, to reduce the coupling between codes, 
    which could make us easier to test and change the code in the future.


# Future development
There are some features I think are worth to add in the future
1. `cpx get average`                                    Get the average of all data of all services on cpx server
2. `cpx get average --service SERVICE`                  Get the average of all data of a specific services on cpx server continuously
3. `cpx watch average`                                  Watch the average of all data of all services on cpx server continuously
4. `cpx watch average --service SERVICE`                Watch the average of all data of a specific services on cpx server continuously
5. `cpx watch average --data DATA --service SERVICE`    Watch the average of a specific data of a specific services on cpx server continuously
6. tls connection between client to server
7. Could use Go to develop this tool as generally the speed of Go is faster. Also, async request and data type validation is out-of-the-box in Go.
8. Make configure function for the command line tool to configure the default settings (e.g. -n default value, server configurations)
