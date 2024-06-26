from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

questions = [
    {
        'question': 'What does TCP stand for in the context of computer networks?',
        'options': ['Transmission Control Protocol', 'Technical Control Protocol', 'Transfer Control Protocol', 'Telecommunication Control Protocol'],
        'correct_option': 'Transmission Control Protocol'
    },
    {
        'question': 'Which device is used to connect multiple networks together?',
        'options': ['Router', 'Modem', 'Switch', 'Bridge'],
        'correct_option': 'Router'
    },
    {
        'question': 'What is the purpose of DNS in computer networks?',
        'options': ['To convert domain names to IP addresses', 'To encrypt network traffic', 'To manage network security', 'To regulate network bandwidth'],
        'correct_option': 'To convert domain names to IP addresses'
    },
    {
        'question': 'Which protocol is used to retrieve email from a remote server?',
        'options': ['SMTP', 'POP3', 'FTP', 'HTTP'],
        'correct_option': 'POP3'
    },
    {
        'question': 'What does HTTP stand for in the context of web browsing?',
        'options': ['HyperText Transfer Protocol', 'High Transfer Protocol', 'Home Transfer Protocol', 'Hyper Transfer Protocol'],
        'correct_option': 'HyperText Transfer Protocol'
    },
    {
        'question': 'What is the function of a firewall in computer networks?',
        'options': ['To block unauthorized access and control incoming and outgoing network traffic', 'To amplify network signals for long-distance transmission', 'To redirect network traffic to optimize performance', 'To secure physical connections between network devices'],
        'correct_option': 'To block unauthorized access and control incoming and outgoing network traffic'
    },
    {
        'question': 'Which network topology connects all devices to a single central point?',
        'options': ['Star', 'Bus', 'Ring', 'Mesh'],
        'correct_option': 'Star'
    },
    {
        'question': 'What is the default subnet mask for a Class C network?',
        'options': ['255.255.255.0', '255.0.0.0', '255.255.0.0', '255.255.255.255'],
        'correct_option': '255.255.255.0'
    },
    {
        'question': 'Which OSI layer is responsible for routing and forwarding data packets?',
        'options': ['Layer 3 (Network Layer)', 'Layer 2 (Data Link Layer)', 'Layer 4 (Transport Layer)', 'Layer 1 (Physical Layer)'],
        'correct_option': 'Layer 3 (Network Layer)'
    },
    {
        'question': 'What is the difference between TCP and UDP?',
        'options': ['TCP provides reliable, connection-oriented communication, while UDP provides unreliable, connectionless communication.', 'TCP is faster than UDP for large file transfers.', 'UDP is more secure than TCP.', 'There is no difference; they are synonyms.'],
        'correct_option': 'TCP provides reliable, connection-oriented communication, while UDP provides unreliable, connectionless communication.'
    },
    {
        'question': 'Which protocol is used to assign IP addresses dynamically on a network?',
        'options': ['DHCP', 'DNS', 'FTP', 'SMTP'],
        'correct_option': 'DHCP'
    },
    {
        'question': 'What is the maximum cable length for Ethernet using twisted pair cabling?',
        'options': ['100 meters', '50 meters', '500 meters', '1000 meters'],
        'correct_option': '100 meters'
    },
    {
        'question': 'Which protocol is used for secure communication over a computer network?',
        'options': ['SSL/TLS', 'HTTP', 'FTP', 'SMTP'],
        'correct_option': 'SSL/TLS'
    },
    {
        'question': 'In which layer of the OSI model does SSL/TLS operate?',
        'options': ['Presentation Layer (Layer 6)', 'Application Layer (Layer 7)', 'Session Layer (Layer 5)', 'Transport Layer (Layer 4)'],
        'correct_option': 'Transport Layer (Layer 4)'
    },
    {
        'question': 'Which protocol is used for file sharing over a network?',
        'options': ['SMB (Server Message Block)', 'SMTP', 'SSH (Secure Shell)', 'SNMP (Simple Network Management Protocol)'],
        'correct_option': 'SMB (Server Message Block)'
    },
    {
        'question': 'What type of attack floods a network with illegitimate traffic to disrupt normal operations?',
        'options': ['DDoS (Distributed Denial of Service)', 'Phishing', 'Man-in-the-Middle', 'SQL Injection'],
        'correct_option': 'DDoS (Distributed Denial of Service)'
    },
    {
        'question': 'Which device operates at Layer 2 of the OSI model and forwards packets based on MAC addresses?',
        'options': ['Switch', 'Router', 'Firewall', 'Hub'],
        'correct_option': 'Switch'
    },
    {
        'question': 'What is the main advantage of VLANs (Virtual Local Area Networks) in networking?',
        'options': ['Improved security and broadcast traffic control', 'Faster data transfer speeds', 'Easier management of network cables', 'Compatibility with older networking standards'],
        'correct_option': 'Improved security and broadcast traffic control'
    },
    {
        'question': 'Which protocol is used to send email between servers?',
        'options': ['SMTP', 'POP3', 'IMAP', 'HTTP'],
        'correct_option': 'SMTP'
    },
    {
        'question': 'What does NAT (Network Address Translation) do?',
        'options': ['Translates private IP addresses to public IP addresses and vice versa', 'Encrypts network traffic for secure transmission', 'Monitors and filters incoming network traffic', 'Manages domain name resolution'],
        'correct_option': 'Translates private IP addresses to public IP addresses and vice versa'
    },
    {
        'question': 'Which type of IP address is used for communication within the same local network?',
        'options': ['Private IP address', 'Public IP address', 'Static IP address', 'Dynamic IP address'],
        'correct_option': 'Private IP address'
    },
    {
        'question': 'What is the primary purpose of ARP (Address Resolution Protocol) in TCP/IP networking?',
        'options': ['To map IP addresses to MAC addresses', 'To encrypt network traffic', 'To authenticate users on the network', 'To route packets between networks'],
        'correct_option': 'To map IP addresses to MAC addresses'
    },
    {
        'question': 'Which encryption protocol secures web traffic using HTTPS?',
        'options': ['SSL/TLS', 'SSH', 'IPSec', 'WPA2'],
        'correct_option': 'SSL/TLS'
    },
    {
        'question': 'What is a MAC address?',
        'options': ['A unique identifier assigned to network interfaces', 'A type of network protocol', 'A standard format for email addresses', 'A special routing table used by routers'],
        'correct_option': 'A unique identifier assigned to network interfaces'
    },
    {
        'question': 'Which protocol resolves IP addresses to hostnames?',
        'options': ['DNS (Domain Name System)', 'DHCP (Dynamic Host Configuration Protocol)', 'ARP (Address Resolution Protocol)', 'SNMP (Simple Network Management Protocol)'],
        'correct_option': 'DNS (Domain Name System)'
    },
    {
        'question': 'What is the purpose of ICMP (Internet Control Message Protocol) in networking?',
        'options': ['To diagnose network issues and report errors', 'To encrypt network traffic', 'To assign IP addresses dynamically', 'To establish secure connections'],
        'correct_option': 'To diagnose network issues and report errors'
    },
    {
        'question': 'Which protocol is used to securely transfer files over a network?',
        'options': ['FTP (File Transfer Protocol)', 'SMTP (Simple Mail Transfer Protocol)', 'HTTP (HyperText Transfer Protocol)', 'SNMP (Simple Network Management Protocol)'],
        'correct_option': 'FTP (File Transfer Protocol)'
    },
    {
        'question': 'What does IP stand for in the context of computer networks?',
        'options': ['Internet Protocol', 'Internal Protocol', 'Interconnect Protocol', 'Intranet Protocol'],
        'correct_option': 'Internet Protocol'
    },
    {
        'question': 'Which type of IP address is typically assigned by a DHCP server?',
        'options': ['Dynamic IP address', 'Static IP address', 'Private IP address', 'Public IP address'],
        'correct_option': 'Dynamic IP address'
    },
    {
        'question': 'What is the purpose of a MAC address?',
        'options': ['To uniquely identify network interfaces', 'To manage IP address allocation', 'To encrypt network traffic', 'To route packets between networks'],
        'correct_option': 'To uniquely identify network interfaces'
    },
    {
        'question': 'Which networking device operates at Layer 1 of the OSI model?',
        'options': ['Hub', 'Router', 'Switch', 'Firewall'],
        'correct_option': 'Hub'
    },
    {
        'question': 'What is the role of DHCP (Dynamic Host Configuration Protocol) in a network?',
        'options': ['To dynamically assign IP addresses to devices', 'To encrypt network traffic', 'To block unauthorized access', 'To create virtual private networks'],
        'correct_option': 'To dynamically assign IP addresses to devices'
    },
    {
        'question': 'Which type of network mask is used to extend the size of a network?',
        'options': ['Subnet mask', 'Gateway mask', 'Broadcast mask', 'Firewall mask'],
        'correct_option': 'Subnet mask'
    },
    {
        'question': 'What is the purpose of a gateway in computer networks?',
        'options': ['To connect different networks', 'To filter spam emails', 'To manage network security', 'To store network backups'],
        'correct_option': 'To connect different networks'
    },
    {
        'question': 'Which protocol is used to remotely access a server or device securely?',
        'options': ['SSH (Secure Shell)', 'FTP (File Transfer Protocol)', 'SMTP (Simple Mail Transfer Protocol)', 'HTTP (HyperText Transfer Protocol)'],
        'correct_option': 'SSH (Secure Shell)'
    },
    {
        'question': 'What is the primary function of a DNS server?',
        'options': ['To translate domain names to IP addresses', 'To compress network traffic', 'To monitor network bandwidth', 'To block malicious websites'],
        'correct_option': 'To translate domain names to IP addresses'
    },
    {
        'question': 'Which networking component is used to regulate data flow between two networks?',
        'options': ['Router', 'Modem', 'Switch', 'Hub'],
        'correct_option': 'Router'
    },
    {
        'question': 'What is the purpose of ARP (Address Resolution Protocol) in networking?',
        'options': ['To map IP addresses to MAC addresses', 'To establish secure connections', 'To manage network traffic', 'To filter unwanted data packets'],
        'correct_option': 'To map IP addresses to MAC addresses'
    },
    {
        'question': 'Which protocol is responsible for ensuring error-free data transmission?',
        'options': ['TCP (Transmission Control Protocol)', 'UDP (User Datagram Protocol)', 'HTTP (HyperText Transfer Protocol)', 'IP (Internet Protocol)'],
        'correct_option': 'TCP (Transmission Control Protocol)'
    },
    {
        'question': 'What is the purpose of NAT (Network Address Translation) in networking?',
        'options': ['To translate private IP addresses to public IP addresses', 'To authenticate users on the network', 'To encrypt network traffic', 'To manage DNS resolution'],
        'correct_option': 'To translate private IP addresses to public IP addresses'
    },
    {
        'question': 'Which OSI layer is responsible for converting data into a format suitable for transmission?',
        'options': ['Presentation Layer (Layer 6)', 'Application Layer (Layer 7)', 'Session Layer (Layer 5)', 'Data Link Layer (Layer 2)'],
        'correct_option': 'Presentation Layer (Layer 6)'
    },
    {
        'question': 'What is the main advantage of using UDP (User Datagram Protocol) over TCP (Transmission Control Protocol)?',
        'options': ['Lower overhead and faster transmission', 'Stronger encryption', 'More reliable data delivery', 'Better support for large file transfers'],
        'correct_option': 'Lower overhead and faster transmission'
    },
    {
        'question': 'Which type of network attack intercepts communication between parties to steal data?',
        'options': ['Man-in-the-Middle (MitM) attack', 'DDoS (Distributed Denial of Service) attack', 'Phishing attack', 'SQL Injection attack'],
        'correct_option': 'Man-in-the-Middle (MitM) attack'
    },
    {
        'question': 'What is the purpose of VLANs (Virtual Local Area Networks) in networking?',
        'options': ['To segment and isolate networks for improved security', 'To speed up network traffic', 'To connect different types of networks', 'To manage network bandwidth'],
        'correct_option': 'To segment and isolate networks for improved security'
    },
    {
        'question': 'Which protocol is used for remotely managing and monitoring network devices?',
        'options': ['SNMP (Simple Network Management Protocol)', 'SMTP (Simple Mail Transfer Protocol)', 'SIP (Session Initiation Protocol)', 'SMB (Server Message Block)'],
        'correct_option': 'SNMP (Simple Network Management Protocol)'
    },
    {
        'question': 'What is the purpose of a proxy server in a network?',
        'options': ['To act as an intermediary between clients and servers', 'To secure wireless networks', 'To manage IP addresses', 'To filter email spam'],
        'correct_option': 'To act as an intermediary between clients and servers'
    }
]


# Shuffle questions randomly
random.shuffle(questions)

# Select 20 random questions from the pool of questions
selected_questions = random.sample(questions, 20)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('answer_selected')
def handle_answer(data):
    question_index = data['question_index']
    selected_option = data['selected_option']
    correct_option = selected_questions[question_index]['correct_option']
    is_correct = (selected_option == correct_option)
    emit('answer_result', {'is_correct': is_correct, 'correct_option': correct_option})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions')
def get_questions():
    return jsonify(selected_questions)

if __name__ == '__main__':
    socketio.run(app, debug=True)
