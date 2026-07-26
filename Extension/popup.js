// popup.js (Definitive Final Version with all fixes)

document.addEventListener('DOMContentLoaded', () => {
  // --- UI Elements ---
  const checkBtn = document.getElementById('checkBtn');
  const urlInput = document.getElementById('urlInput');
  const resultDiv = document.getElementById('result');
  // ... and all other UI elements ...
  const expandBtn = document.getElementById('expandBtn');
  const tinyUrlInput = document.getElementById('tinyUrlInput');
  const expandResultDiv = document.getElementById('expandResult');
  const lockdownBtn = document.getElementById('lockdownBtn');
  const lockdownStatus = document.getElementById('lockdownStatus');
  const phishingTodayEl = document.getElementById('phishingToday');
  const safeTodayEl = document.getElementById('safeToday');
  const lifetimeTotalEl = document.getElementById('lifetimeTotal');
  const assistantIconBtn = document.getElementById('assistant-icon-btn');
  const chatModal = document.getElementById('chat-modal');
  const closeChatBtn = document.getElementById('close-chat');
  const chatHistory = document.getElementById('chat-history');
  const chatInput = document.getElementById('chat-input');
  const sendChatBtn = document.getElementById('send-chat-btn');

  // =======================================================
  // VIRTUAL ASSISTANT KNOWLEDGE BASE (CORRECTED STRUCTURE)
  // =======================================================

  // STEP 1: Define the core knowledge with unique entries.
  const KNOWLEDGE_BASE = {
    // This is the FULL, unabridged list of topics.
    'cybersecurity': { answer: "<b>Cybersecurity</b> is the practice of protecting computers, servers, networks, and data from malicious attacks.", example: "<b>Example:</b> Using this extension and having an antivirus are parts of your cybersecurity." },
    'privacy': { answer: "<b>Privacy</b> is your right to control your personal information—who can see, use, and share data about you.", example: "<b>Example:</b> Using our 'Privacy Lockdown' feature helps protect your privacy from websites." },
    'security vs privacy': { answer: "<b>Security vs. Privacy:</b> Security protects your data from attackers (a lock on a door). Privacy controls who has permission to use your data (who gets a key).", example: "<b>Example:</b> A strong password is for <b>security</b>. Not giving your email to every site is for <b>privacy</b>." },
    'cyber': { answer: "The prefix <b>'Cyber'</b> relates to the digital world of computers, information technology, and virtual reality.", example: "<b>Example:</b> A 'cyber-attack' is an attack that happens in the digital world." },
    'phishing': { answer: "<b>Phishing</b> is where scammers impersonate a trusted company to trick you into giving them personal info on a fake website.", example: "<b>Example:</b> An email that looks like it's from your bank, asking you to click a link and 'verify' your password." },
    'vishing': { answer: "<b>Vishing</b> (Voice Phishing) is a phishing attack done over the phone, where scammers pretend to be someone official.", example: "<b>Example:</b> A call from someone claiming to be from tech support, asking for remote access to your PC." },
    'smishing': { answer: "<b>Smishing</b> (SMS Phishing) is an attack using text messages, often with a link to a malicious website.", example: "<b>Example:</b> A text saying 'Your package has a customs fee. Pay here: [fake_link].'" },
    'malicious file': { answer: "A <b>Malicious File</b> is any file designed to harm your computer when opened. It can look like a normal PDF or document.", example: "<b>Example:</b> An email with an attachment named 'Invoice.pdf' that secretly installs a virus when opened." },
    'ransomware': { answer: "<b>Ransomware</b> is malware that encrypts your files. The attackers then demand a ransom (payment) to unlock them.", example: "<b>Example:</b> You open a bad attachment, and suddenly all your photos are locked. A popup appears demanding money." },
    'spyware': { answer: "<b>Spyware</b> is malware that secretly spies on you, recording your keystrokes, browsing history, and personal information.", example: "<b>Example:</b> A 'free' game you installed is also secretly recording every website you visit." },
    'social engineering': { answer: "<b>Social Engineering</b> is the art of manipulating people to give up confidential information, relying on psychology instead of hacking.", example: "<b>Example:</b> A scammer calls you pretending to be a colleague and asks for a password, creating a fake sense of urgency." },
    'two-factor authentication': { answer: "<b>Two-Factor Authentication (2FA)</b> adds a second security layer. After your password, you must provide a second code, usually from your phone.", example: "<b>Example:</b> When you log into Google, it asks for a code from your authenticator app. That's 2FA." },
    'vpn': { answer: "A <b>VPN (Virtual Private Network)</b> encrypts your internet traffic and hides your IP address, creating a secure tunnel for your data.", example: "<b>Example:</b> At a coffee shop, using a VPN prevents others on the Wi-Fi from snooping on your activity." },
    'firewall': { answer: "A <b>Firewall</b> is a security guard for your network. It monitors traffic and blocks malicious connections based on a set of rules.", example: "<b>Example:</b> Your Windows or Mac computer has a built-in firewall that helps block hackers from the internet." },
    'imei': { answer: "An <b>IMEI</b> is a unique 15-digit number that identifies a specific mobile phone, used to track stolen devices.", example: "<b>Example:</b> You can find your phone's IMEI by dialing *#06#." },
    'ip address': { answer: "An <b>IP Address</b> is like a mailing address for your computer on the internet, allowing it to send and receive data.", example: "<b>Example:</b> When you visit google.com, your request is sent from your IP address to Google's." },
    'mac address': { answer: "A <b>MAC Address</b> is a unique hardware serial number for your device's network card (like for Wi-Fi or Ethernet).", example: "<b>Example:</b> Your home Wi-Fi router uses MAC addresses to manage connected devices." },
    'footprints': { answer: "<b>Digital Footprints</b> are the trail of data you leave behind online, including websites visited, emails sent, and social media posts.", example: "<b>Example:</b> Your Google search history is a part of your digital footprint." },
    'evidence collection': { answer: "<b>Evidence Collection</b> in cybersecurity is the process of gathering and preserving digital data in a legally admissible way.", example: "<b>Example:</b> Making a perfect, bit-by-bit copy of a suspect's hard drive before analyzing it." },
    'internet': { answer: "The <b>Internet</b> is the massive, global network of connected computers—the physical infrastructure of cables, servers, and routers.", example: "<b>Example:</b> The internet is the 'highway system' for digital information." },
    'web': { answer: "The <b>World Wide Web (WWW)</b> is the collection of websites and pages that you access *using* the internet.", example: "<b>Example:</b> The web is the collection of 'cities and buildings' along the internet highway." },
    'surface web': { answer: "The <b>Surface Web</b> is the part of the web indexed by search engines like Google. It's the 'tip of the iceberg' that is easily accessible.", example: "<b>Example:</b> Wikipedia and news sites are on the Surface Web." },
    'deep web': { answer: "The <b>Deep Web</b> is the part of the web not indexed by search engines. You need a login or direct URL. It's not illegal; it's just private.", example: "<b>Example:</b> Your online banking portal and your email inbox are part of the Deep Web." },
    'dark web': { answer: "The <b>Dark Web</b> is a small part of the Deep Web that requires special software (like Tor) to access. It offers anonymity and is often used for illegal activities.", example: "<b>Example:</b> Illicit marketplaces exist on the Dark Web." },
    'marianas web': { answer: "The <b>Marianas Web</b> is an urban legend. It's a supposed 'deepest' part of the web, but there is no evidence it actually exists.", example: "<b>Example:</b> Stories about the Marianas Web are just stories." },
    'copyright': { answer: "<b>Copyright</b> is a legal right giving the creator of an original work (like a photo or software) exclusive rights to its use.", example: "<b>Example:</b> You can't use a famous song in your video without permission due to copyright." },
    'cybersecurity acts': { answer: "In India, the primary law is the <b>Information Technology (IT) Act, 2000</b>. It provides the legal framework for e-commerce and cybercrime.", example: "<b>Example:</b> If someone hacks your email, they can be prosecuted under the IT Act." },
    'antivirus': { answer: "An <b>Antivirus</b> is a program designed to detect, prevent, and remove malware from your computer.", example: "<b>Example:</b> Windows Defender and Norton are popular antivirus programs." },
    'legitimate website': { answer: "A <b>Legitimate Website</b> is a genuine, trustworthy site. Identifying them is a key security skill.", example: "<b>Tips to Spot a Legitimate Site:</b><br>1. Check the URL for `https://` and typos.<br>2. Look for a professional design.<br>3. Real sites have clear 'Contact Us' & 'About Us' pages." },
    'this extension': { answer: "I am your personal AI security assistant! I automatically check websites for threats. Ask me anything about cybersecurity.", example: "<b>Example:</b> Just browse the web, and I'll block dangerous sites for you automatically!" },
    'privacy lockdown': { answer: "The <b>Privacy Lockdown</b> instantly hardens your browser's security by blocking cookies, trackers, and intrusive permissions like camera and location access.", example: "<b>Example:</b> Click 'Engage Privacy Lockdown' to make your browser much more private." },
    'enhance your privacy': { answer: "<b>Browser Hardening Tips:</b><br>1. Use the 'Privacy Lockdown' button below.<br>2. Regularly clear your browsing data.<br>3. Be mindful of the extensions you install.", example: "<b>Example:</b> Engaging the lockdown is the fastest way to enhance your privacy." },
    'security tips': { answer: "<b>Essential Security Tips:</b><br>1. <b>Use Strong, Unique Passwords:</b> Never reuse passwords across different websites. Use a password manager to keep track of them.<br>2. <b>Enable Two-Factor Authentication (2FA):</b> This is the single best thing you can do to protect your accounts.<br>3. <b>Be Wary of Downloads:</b> Only download software from official websites and app stores.<br>4. <b>Keep Software Updated:</b> Always install updates for your browser, operating system, and applications to patch security holes.", example: "<b>Example:</b> If a hacker steals your password for one site, using unique passwords for other sites means your other accounts are still safe." },
    'security': { answer: "<b>Security</b>, in a digital context, is the practice of defending systems, networks, and data from unauthorized access or criminal use. It's about building defenses to keep attackers out.", example: "<b>Example:</b> Having a firewall on your computer is a form of security. It acts like a digital guard, blocking suspicious connections from the internet." },
    'virus': { answer: "A <b>Virus</b> is a type of malicious code that attaches itself to a legitimate program. When you run that program, the virus also runs, often spreading itself to other programs on your computer.", example: "<b>Example:</b> Imagine a virus infects your calculator app. Every time you open the calculator, the virus copies itself to another program, like your web browser. It's a digital infection." },
    'malware': { answer: "<b>Malware</b> (short for Malicious Software) is the general name for ANY software designed to cause harm. Viruses are just one type of malware.", example: "<b>Example:</b> Malware is the 'umbrella' term. It includes viruses, spyware (which spies on you), ransomware (which locks your files), and adware (which spams you with ads)." },
    'cloning': { answer: "In cybersecurity, <b>Cloning</b> usually refers to 'website cloning.' This is a technique where attackers make an exact, pixel-for-pixel copy of a legitimate website (like a bank login page) to create a highly convincing phishing site.", example: "<b>Example:</b> A hacker clones your bank's login page and hosts it at 'your-bank-login.net'. When you enter your password there, they steal it. Our AI model is trained to spot these clones." },
    'buffer overflow': { answer: "A <b>Buffer Overflow</b> is a classic and powerful type of software bug. It happens when a program tries to put more data into a temporary storage area (a 'buffer') than it can hold. The extra data spills over and can overwrite other parts of the computer's memory.", example: "<b>Example:</b> Imagine a form asks for your 4-digit PIN, but a hacker enters 100 digits. If the program is poorly written, those extra 96 digits could spill out and be used to crash the program or even run malicious code." },
    'url': { answer: "A <b>URL</b> (Uniform Resource Locator) is the unique address for a resource on the internet. It's like a complete street address for a specific house on a specific street in a specific city.", example: "<b>Example:</b> In `https://www.google.com/search`, 'https://' is the protocol, 'www.google.com' is the domain, and '/search' is the path to a specific page." },
    'url features': { answer: "<b>URL Features</b> are the specific characteristics of a URL that our AI models analyze to determine if it's safe or phishing. We don't just look at the name; we look at its deep structure.", example: "<b>Example:</b> Our AI analyzes features like URL length, the number of subdomains, the randomness of characters (entropy), and the presence of suspicious words like 'login' or 'secure'." },
  };

  // STEP 2: Create aliases AFTER the main object is defined. This is the fix.
  KNOWLEDGE_BASE['cyber security'] = KNOWLEDGE_BASE['cybersecurity'];
  KNOWLEDGE_BASE['privacy vs security'] = KNOWLEDGE_BASE['security vs privacy'];
  KNOWLEDGE_BASE['viruses'] = KNOWLEDGE_BASE['virus'];
  KNOWLEDGE_BASE['2fa'] = KNOWLEDGE_BASE['two-factor authentication'];
  KNOWLEDGE_BASE['safe website'] = KNOWLEDGE_BASE['legitimate website'];
  KNOWLEDGE_BASE['cyber-security'] = KNOWLEDGE_BASE['cybersecurity'];

  const ALL_KEYWORDS = Object.keys(KNOWLEDGE_BASE);

  // --- Chat Modal Event Listeners & Logic ---
  assistantIconBtn.addEventListener('click', () => { chatModal.style.display = 'block'; });
  closeChatBtn.addEventListener('click', () => { chatModal.style.display = 'none'; });
  window.addEventListener('click', (event) => { if (event.target == chatModal) chatModal.style.display = 'none'; });
  sendChatBtn.addEventListener('click', handleSendMessage);
  chatInput.addEventListener('keydown', (event) => { if (event.key === 'Enter') handleSendMessage(); });

  function handleSendMessage() {
    const userText = chatInput.value.trim();
    if (!userText) return;
    appendMessage(userText, 'user');
    chatInput.value = '';
    const assistantResponse = getAssistantResponse(userText);
    setTimeout(() => { appendMessage(assistantResponse, 'assistant'); }, 300);
  }

  function appendMessage(html, sender) {
    const messageWrapper = document.createElement('div');
    messageWrapper.className = `chat-message ${sender}-message`;
    messageWrapper.innerHTML = html;
    chatHistory.appendChild(messageWrapper);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }
  
  // --- NEW, SMARTER RESPONSE LOGIC ---
  function getAssistantResponse(command) {
    command = command.toLowerCase().trim();

    // --- NEW, SMARTER GREETING CHECKER ---
    const GREETING_KEYWORDS = [
      'hi', 'hello', 'hey', 'yo', 'howdy', 'greetings',
      'good morning', 'good afternoon', 'good evening',
      'how are you', "how's it going", "what's up",
      'can you help', 'i have a question'
    ];

    // Check if the user's command contains any of our greeting keywords
    const isGreeting = GREETING_KEYWORDS.some(keyword => command.startsWith(keyword));

    if (isGreeting) {
      return "<b>Hi friend!</b> I'm your AI security assistant. How can I help you today? You can ask me about topics like <b>phishing, malware, 2FA,</b> or for <b>safety tips</b>.";
    }

    let bestMatch = '';
    // Find the longest keyword that exists in the user's command
    for (const keyword of ALL_KEYWORDS) {
      if (command.includes(keyword)) {
        if (keyword.length > bestMatch.length) {
          bestMatch = keyword;
        }
      }
    }

    if (bestMatch) {
      const entry = KNOWLEDGE_BASE[bestMatch];
      return `${entry.answer}<br><br>${entry.example}`;
    }
    
    return "I'm sorry, I don't have information on that topic. I can help with a wide range of common cybersecurity concepts.";
  }

  // --- ALL OTHER FUNCTIONS (UNCHANGED) ---
  function updateStatsDisplays(){chrome.storage.local.get(["safeCount","phishingCount","lastReset","lifetimeTotal"],(t)=>{const e=(new Date).toISOString().split("T")[0];let o=t.safeCount||0,n=t.phishingCount||0,s=t.lifetimeTotal||0;t.lastReset!==e&&(o=0,n=0),phishingTodayEl.textContent=n,safeTodayEl.textContent=o,lifetimeTotalEl.textContent=s})}
  checkBtn.addEventListener('click',function(){const t=urlInput.value.trim();t&&(resultDiv.textContent="Checking...",resultDiv.style.display="block",fetch("http://127.0.0.1:5000/predict",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:t})}).then(t=>t.json()).then(t=>{resultDiv.className="result-area",t.result==="PHISHING"?(resultDiv.classList.add("phishing"),resultDiv.textContent=`PHISHING`):t.result==="SAFE"?(resultDiv.classList.add("safe"),resultDiv.textContent=`SAFE`):(resultDiv.classList.add("phishing"),resultDiv.textContent=`Error: ${t.reason}`)}).catch(t=>{resultDiv.classList.add("phishing"),resultDiv.textContent="Error: Could not connect to server."}))});
  expandBtn.addEventListener('click',function(){const t=tinyUrlInput.value.trim();t&&(expandResultDiv.textContent="Expanding...",expandResultDiv.style.display="block",fetch("http://127.0.0.1:5000/expand",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:t})}).then(t=>t.json()).then(t=>{expandResultDiv.className="result-area",t.expanded_url?expandResultDiv.textContent=`Expanded: ${t.expanded_url}`:(expandResultDiv.classList.add("phishing"),expandResultDiv.textContent=`Error: ${t.error}`)}).catch(t=>{expandResultDiv.classList.add("phishing"),expandResultDiv.textContent="Error: Could not connect to server."}))});
  const permissionsToBlock=["location","camera","microphone","sensors","automaticDownloads","usbDevices","serialPorts","hidDevices","fileSystemAccess","clipboard","paymentHandler","ar","vr","windowManagement","popups","ads","sound"];function updateButtonState(){chrome.privacy.websites.thirdPartyCookiesAllowed.get({},function(t){!1===t.value?(lockdownBtn.textContent="Disable Privacy Lockdown",lockdownBtn.style.backgroundColor="#28a745"):(lockdownBtn.textContent="Engage Privacy Lockdown",lockdownBtn.style.backgroundColor="#dc3545")})}lockdownBtn.addEventListener("click",function(){lockdownBtn.disabled=!0,lockdownStatus.style.display="block",lockdownStatus.textContent="Applying settings...",chrome.privacy.websites.thirdPartyCookiesAllowed.get({},function(t){const e=!1!==t.value,o=[];e?(o.push(new Promise(t=>chrome.privacy.websites.thirdPartyCookiesAllowed.set({value:!1},t))),o.push(new Promise(t=>chrome.privacy.websites.doNotTrackEnabled.set({value:!0},t))),permissionsToBlock.forEach(t=>{chrome.contentSettings[t]&&o.push(new Promise(e=>chrome.contentSettings[t].set({primaryPattern:"<all_urls>",setting:"block"},e)))})):(o.push(new Promise(t=>chrome.privacy.websites.thirdPartyCookiesAllowed.clear({},t))),o.push(new Promise(t=>chrome.privacy.websites.doNotTrackEnabled.clear({},t))),permissionsToBlock.forEach(t=>{chrome.contentSettings[t]&&o.push(new Promise(e=>chrome.contentSettings[t].clear({},e)))})),Promise.all(o).then(()=>{lockdownStatus.textContent=e?"Settings Applied: Lockdown Engaged!":"Settings Applied: Lockdown Disabled.",lockdownBtn.disabled=!1,updateButtonState()})})});

  // --- Initialize The Popup ---
  updateStatsDisplays();
  updateButtonState();
});