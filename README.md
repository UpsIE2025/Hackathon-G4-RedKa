# Hackathon-G4-RedKa
G4 Hackathon Repository

## 📂 Project Overview

This repository contains the work done by Group 4 during the hackathon.   
The focus of the hackathon was on different types of message channels and message construction patterns, including:

- **Dead Letter Channel**
- **Invalid Message Channel**
- **Point-to-Point Channel**
- **Channel Adapter** (implemented by AdrianC47)

## 📌 Message Channels and Patterns

### Channel Adapter
A Channel Adapter allows an application to connect to a message channel without knowing the details of the channel itself. It acts as a bridge between the application and the messaging system.

### Data Type Channel
A Data Type Channel is used to route messages based on their data type. This ensures that messages of a specific type are processed by the appropriate consumer.

### Dead Letter Channel
A Dead Letter Channel is used to handle messages that cannot be processed successfully. These messages are routed to a separate channel for further analysis or reprocessing.

### Guaranteed Delivery
Guaranteed Delivery ensures that a message is delivered to the intended recipient even in the case of system failures. This pattern often involves message persistence and retries.

### Invalid Message Channel
An Invalid Message Channel is used to handle messages that do not conform to the expected format or schema. These messages are routed to a separate channel for validation and correction.

### Message Bus
A Message Bus is a central channel that allows multiple applications to communicate with each other. It decouples the sender and receiver, enabling scalable and flexible communication.

### Point-to-Point Channel
A Point-to-Point Channel ensures that a message is delivered to exactly one receiver. This pattern is useful for scenarios where a message should be processed by a single consumer.

### Publish-Subscribe Channel
A Publish-Subscribe Channel allows multiple consumers to receive messages from a single channel. This pattern is useful for broadcasting messages to multiple subscribers.

