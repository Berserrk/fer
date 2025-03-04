{
    "Barack Obama": "Former President of the United States, known for the Affordable Care Act",
    "Michelle Obama": "Former First Lady, author of 'Becoming', advocate for healthy eating",
    "Barack H. Obama": "44th President of the USA, Nobel Peace Prize winner",
    "B. Obama": "Ex-U.S. President, first African-American president",
    "Elon Musk": "CEO of Tesla and SpaceX, known for pushing AI and space exploration",
    "E. Musk": "Founder of SpaceX, advocate for interplanetary travel, CEO of Tesla",
    "Jeff Bezos": "Founder of Amazon, space entrepreneur",
    "J. Bezos": "Blue Origin founder, billionaire investor",
    "Jeffrey Bezos": "E-commerce pioneer, owner of The Washington Post",
    "Bill Gates": "Co-founder of Microsoft, philanthropist",
    "William Gates": "Tech mogul, founded the Bill & Melinda Gates Foundation",
    "B. Gates": "Billionaire investor, software pioneer, Microsoft co-founder",
    "Steve Jobs": "Apple co-founder, known for revolutionizing smartphones",
    "Steven P. Jobs": "Visionary entrepreneur, led Apple’s innovation",
    "Tim Cook": "Current CEO of Apple, advocate for privacy and sustainability",
    "T. Cook": "Apple leader, successor to Steve Jobs",
    "Warren Buffett": "Investor, CEO of Berkshire Hathaway, known for value investing",
    "W. Buffett": "Financial guru, longtime leader at Berkshire Hathaway",
    "Sergey Brin": "Google co-founder, AI researcher",
    "Larry Page": "Google co-founder, Alphabet executive",
    "L. Page": "Search engine innovator, AI-focused entrepreneur",
    "Bernie Sanders": "U.S. Senator, advocate for progressive policies",
    "Bernard Sanders": "Politician known for advocating Medicare for All",
    "Joe Biden": "46th President of the United States",
    "J. Biden": "Current U.S. President, formerly Vice President under Obama",
    "Jordan Peterson": "Psychologist, known for self-help books and cultural commentary",
    "Jordan B. Peterson": "Canadian professor, author of '12 Rules for Life'",
    "Peter Jordanson": "Influential speaker on self-improvement and social issues",
    "Richard Branson": "Founder of Virgin Group, billionaire entrepreneur",
    "Dick Branson": "Business magnate, known for Virgin Airlines",
    "Rick Branson": "Investor and adventurer, linked to the Virgin brand"
}


You are an AI that processes a dictionary of entity names and descriptions to group 
similar entities based on name variations and description similarities. Your goal is to:
1. Iterate over each entity in the dictionary using a for loop.
2. Compare its description with every other entity’s description.
3. Group entities that refer to the same person while keeping distinct entities separate, even if they have similar descriptions.
4. Return the output as a JSON object where each key is a unique entity and the value is a list of grouped names.

