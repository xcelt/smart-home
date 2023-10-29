# Smart Home Prototype (SSA 2023)
The following program is a prototype for The Smart Home by The A Team (Group 1) to satify the requirements of Assignment 2 of the Secure System Architecture module. The program comprises an initialiser, server, and client hub, and has been encrypted with RSA and Fernet keys. The focus of the project hypothesis question are the veracity of these keys' security as compared to SHA512.

## Setup
### Prerequisites
* Python ^3.10

### Installing
1. Install the required dependencies in `requirements.txt`:
2. 
   ` `pip install -r requirements.txt` (Windows) || `pip3 install -r requirements.txt`
   
3. Run `python initialise.py` (Windows) || `python3 initialise.py` (Linux)

This will initialise the RSA and Ferent keys for encryption.

[! initialise.py](./images/initialise)

## Run the Program
On a separate terminal each:
1. Run `python deviceservice.py` || `python3 deviceservice.py`
2. Run `python hub.py` || 'python3 hub.py`

Device simulation is set by running `deviceservice.py`. 

[! deviceservice.py](./images/deviceservice)

Device settings can be manipulated by interacting with the client interface in `hub.py` 

[! hub](./images/hub)

## Assumptions
1. For the purpose of this proof of concept demo, the devices are assumed to use the same set of public and private encryption keys
   
## Testing
### Program testing


## Discussion
Testing the ability of RSA and Ferent encryption to withstand hash identification is at the heart of this project. Our team sought to build a comprehensive clienthub and server that could simulate actual smart device use, and then encrypt that program. Our goal was then to demonstrate that RSA and Ferent encryption hashes were harder to crack than SHA512 hashes. 

RSA was chosen as an encryption key (Hamza & Kumar, 2020) because 
* it is asymmetric and has both public and private keys
* the Diffiee-Hellman algorithm "is a key component of the framework" (Tang & Zhou, 2011: )

Forent was chosen as an encryption key (Pronika & Tyagi, 2021) because 
* it is symmetrical and a "lightweight method based on AES-128-CBC" (Asaad et al., 2022: 1)
* this algorithm is intended for constrained IoT devices not unlike the simulated devices in our code.

SHA512 was chosen as a control encryption key because
* it is standardized by NIST (Dobraunig et al, 2015)
* it is the "most widely used hash function" (Ambat et al, 2020), and is considered more secure than other hash functions

### Hypothesis Testing

Proving the veracity of an encryption algorithm can be difficult outside the realm of mathematics, so our group decided to take a hacker mindset to testing. We would see how easy each hash was to identify, as once the type of hash encryption is known bruteforcing is quite simple.

To set a null hypothesis, we took a piece of code from an unused earlier version of our project and implemented SHA512 to encrypt some passwords and ran the program to generate a hash:

[! SHA512 Code](./images/SHA512.png)

[! SHA512 Hash](./images/SHA512hash.png)

We then ran this hash through the popular command line tool _Hashid_ (xxxx, xxxx), which can determine the type of hash presented to be further decrypted by bruteforcing tools like _Hashcat_ (xxxx,). This resulted in a positive hit in the system, correctly determining the hash to be SHA512:

[! Hashid512](./images/hashid512)

The real-world effort to cracking this hash would be minimal, and those without much hacking skill would be able to figure out how to do so from a hacking tutorial on Youtube (XXXX, XXXX).

We then repeated the process for the RSA and Fernet hashes, which were provided during initialisation. Both hashes were unknown in the _hashid_ system:

[! HashidRSA](./images/hashidRSA.png)
[!HashFERN](./images/hashidFERN.png)


# References
* 
