<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px;">

  <h1>📞 Telephone API</h1>
  <p><strong>Telephone</strong> is a simple personal API designed to retrieve detailed information about phone numbers.<br>
  It uses the <a href="https://www.twilio.com/lookup" target="_blank">Twilio Lookup API</a> under the hood to provide accurate and reliable phone number data such as carrier, line type, country, and more.</p>

  <hr>

  <h2>🚀 Features</h2>
  <ul>
    <li>📱 Get carrier and line type information</li>
    <li>🌍 Identify the country and region of a phone number</li>
    <li>🔎 Validate phone numbers before using them</li>
    <li>🧩 Simple and easy-to-use REST API</li>
  </ul>

  <hr>

  <h2>🛠️ Requirements</h2>
  <ul>
    <li><a href="https://www.docker.com/">Docker</a> installed</li>
    <li>A <a href="https://www.twilio.com/">Twilio account</a> and API credentials</li>
  </ul>

  <hr>

  <h2>⚙️ Installation</h2>
  <ol>
    <li>Clone the repository:
      <pre><code>git clone https://github.com/yourusername/telephone.git
cd telephone</code></pre>
    </li>
    <li>Set up your environment variables (e.g., <code>TWILIO_SID</code>, <code>TWILIO_AUTH_TOKEN</code>) in a <code>.env</code> file.</li>
    <li>Compile the project:
      <pre><code>make compile</code></pre>
    </li>
  </ol>

  <hr>

  <h2>🐳 Docker Commands</h2>
  <p>You can manage the project easily with Docker using the following commands:</p>

  <table border="1" cellpadding="8" cellspacing="0">
    <thead>
      <tr>
        <th>Command</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>make compile</code></td>
        <td>Compile the project inside the container.</td>
      </tr>
      <tr>
        <td><code>make build</code></td>
        <td>Build the Docker image.</td>
      </tr>
      <tr>
        <td><code>make up</code></td>
        <td>Start the API service.</td>
      </tr>
      <tr>
        <td><code>make down</code></td>
        <td>Stop and remove containers.</td>
      </tr>
      <tr>
        <td><code>make run</code></td>
        <td>Run the project (equivalent to <code>make up</code>).</td>
      </tr>
    </tbody>
  </table>

  <hr>

  <h2>📡 API Usage</h2>
  <p>Once the service is running, you can make requests like:</p>

  <pre><code>GET /lookup?phone=+15551234567</code></pre>

  <h3>Example Response</h3>
  <pre><code>{
  "phone_number": "+15551234567",
  "country": "US",
  "carrier": "Verizon Wireless",
  "line_type": "mobile",
  "valid": true
}</code></pre>

  <hr>

  <h2>🧪 Development</h2>
  <ol>
    <li>Make sure Docker is running.</li>
    <li>Run the service locally with:
      <pre><code>make up</code></pre>
    </li>
    <li>The API will be available at <code>http://localhost:8000</code> (or your configured port).</li>
  </ol>

  <hr>

  <h2>📄 License</h2>
  <p>This is a <strong>personal project</strong> and not intended for production use.<br>
  Feel free to fork and modify it for your own needs.</p>

</body>
</html>
