import { NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';
import fs from 'fs/promises';
import path from 'path';

// Initialize Gemini API
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

export async function POST(request) {
  try {
    const { query } = await request.json();

    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }

    // Load the AWS documentation JSON
    const jsonPath = path.join(process.cwd(), 'public', 'boto3_docs.json');
    const jsonData = await fs.readFile(jsonPath, 'utf-8');
    const awsDocs = JSON.parse(jsonData);

    // Initialize Gemini model
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    // Step 1: Determine which AWS services are needed
    console.log('Step 1: Identifying relevant AWS services...');
    const serviceNames = Object.keys(awsDocs.services);
    
    const servicePrompt = `You are an AWS expert. Given a user query, identify which AWS service(s) from the list below are needed to accomplish the task.

User Query: "${query}"

Available AWS Services:
${serviceNames.join(', ')}

Respond with ONLY a JSON array of service names that are relevant. Use the exact names from the list above.
Example response format: ["S3", "DynamoDB"]

If no services match, respond with an empty array: []`;

    const serviceResult = await model.generateContent(servicePrompt);
    const serviceResponse = serviceResult.response.text();
    
    // Parse service names from response
    const selectedServices = JSON.parse(serviceResponse.trim());
    console.log('Selected services:', selectedServices);

    if (selectedServices.length === 0) {
      return NextResponse.json(
        { error: 'No relevant AWS services found for your query' },
        { status: 400 }
      );
    }

    // Step 2: For each service, determine which methods are needed
    console.log('Step 2: Identifying relevant methods for each service...');
    const methodsByService = {};

    for (const serviceName of selectedServices) {
      const service = awsDocs.services[serviceName];
      if (!service) continue;

      const methodNames = Object.keys(service.methods);
      
      const methodPrompt = `You are an AWS expert. Given a user query and a list of available methods for the ${serviceName} service, identify which method(s) are needed.

User Query: "${query}"

Available methods for ${serviceName}:
${methodNames.join(', ')}

Respond with ONLY a JSON array of method names that are relevant. Use the exact names from the list above.
Example response format: ["create_bucket", "put_object"]

If no methods match, respond with an empty array: []`;

      const methodResult = await model.generateContent(methodPrompt);
      const methodResponse = methodResult.response.text();
      
      const selectedMethods = JSON.parse(methodResponse.trim());
      console.log(`Selected methods for ${serviceName}:`, selectedMethods);
      
      if (selectedMethods.length > 0) {
        methodsByService[serviceName] = selectedMethods;
      }
    }

    // Step 3: Gather full documentation for selected methods
    console.log('Step 3: Gathering documentation for selected methods...');
    const methodDocs = [];

    for (const [serviceName, methods] of Object.entries(methodsByService)) {
      for (const methodName of methods) {
        const methodDoc = awsDocs.services[serviceName].methods[methodName];
        if (methodDoc) {
          methodDocs.push({
            service: serviceName,
            method: methodName,
            ...methodDoc
          });
        }
      }
    }

    // Step 4: Generate Python code using the documentation
    console.log('Step 4: Generating Python code...');
    
    const documentationContext = methodDocs.map(doc => `
Service: ${doc.service}
Method: ${doc.method}
Description: ${doc.description}
Syntax: ${doc.syntax}
Parameters: ${JSON.stringify(doc.parameters, null, 2)}
Returns: ${doc.returns}
${doc.examples && doc.examples.length > 0 ? `Examples:\n${doc.examples.join('\n\n')}` : ''}
    `).join('\n---\n');

    const codePrompt = `You are an expert Python developer specializing in AWS Boto3. Generate clean, production-ready Python code to accomplish the following task.

User Query: "${query}"

AWS Documentation for relevant methods:
${documentationContext}

Requirements:
1. Import necessary boto3 modules
2. Include proper error handling
3. Add helpful comments
4. Use best practices for AWS SDK usage
5. Include any necessary configuration (regions, credentials setup hints)
6. Make the code complete and executable

Generate ONLY the Python code, no explanations or markdown formatting. Start directly with the imports.`;

    const codeResult = await model.generateContent(codePrompt);
    const pythonCode = codeResult.response.text();

    // Clean up the code (remove markdown if present)
    let cleanCode = pythonCode.trim();
    if (cleanCode.startsWith('```python')) {
      cleanCode = cleanCode.replace(/^```python\n/, '').replace(/\n```$/, '');
    } else if (cleanCode.startsWith('```')) {
      cleanCode = cleanCode.replace(/^```\n/, '').replace(/\n```$/, '');
    }

    console.log('Code generation complete!');

    return NextResponse.json({
      success: true,
      query,
      servicesUsed: selectedServices,
      methodsUsed: methodsByService,
      code: cleanCode
    });

  } catch (error) {
    console.error('Error in code generation:', error);
    return NextResponse.json(
      { 
        error: 'Failed to generate code', 
        details: error.message 
      },
      { status: 500 }
    );
  }
}

// Optional: Add GET endpoint for health check
export async function GET() {
  return NextResponse.json({ 
    status: 'OK', 
    message: 'AWS Code Generator API is running' 
  });
}
