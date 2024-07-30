# TinyJSON Test Suite

## Description

TinyJSON is a program written in Python from scratch without using json library that allow user to parse JSON string data from JSON file into Python data type. However, the purpose of this assignment is to create a test suite that test this program by properties based testing using tools like Hypothesis and Icontract library for automation testing to generate random input that can cover unexpect case as much as we can without manually crafting the test input.

## About

TinyJSON and its test suite is a program dedicated to educational purpose only. This project allow me to develop my software testing skill using properties-based testing like Hypothesis and Icontract within Python library. Since this is only a part for university project at USYD - SOFT3202 Software Construction and Design 2 given by the task:
>  Your task is to write properties and contracts for a program called tinyJSON using hypothesis and icontract, property-based testing frameworks shown to you in the lectures and tutorials for this unit. The goal is to verify the provided properties and contracts achieve a specific statement coverage threshold when tested. - USYD

The scaffold also provide with the [code base](https://edstem.org/au/courses/15196/lessons/52928/slides/359516) (Only USYD student able to access the code base)

## Goals and Knowledge outcome

During the development of this test suite I had gain an understanding of
- properties based testing in Python
- Automation in testing
- Unit testing

## How to run the test suite

1. Download this repo to your local machine
2. Open terminal on the directory that you've download this repo
3. Install Hypothesis and Icontract by type
```
pip install hypothesis'
```
and
```
pip install icontract
```
in terminal. Note that this assume you had pip install on your machine and if not please try to find a way to install pip otherwise finding other way to install those library on your own.

4. Run the test suite by type ```python test.py```
5. You can see that there's 22 test running in your terminal and message 'OK'

## Contributor

I declare here that TinyJSON is not a program made by me but written by Usyd staff.

USYD: https://www.sydney.edu.au/

## Credit

I only did everything from 'test.py' file and did not change anything from 'tinyJSON.py' as my task is only provide the test suite for it.

Programmer: Best Phanuwish