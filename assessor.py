 
from crawl4ai import *
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
import asyncio
from colorama import Fore

from dotenv import load_dotenv
load_dotenv()

import logfire
logfire.configure()

import sys
sys.path.append('.')


class assessmentDeps:
    policyID: str

assessmentAgent = Agent("openai:o3-mini", 
                        system_prompt="you are underwriter that based on the customer declaration, and for each declaration and medical finding, cross check with the get_web_info result, in order to provide an underwriting decision",
                        deps_type=assessmentDeps)

@assessmentAgent.tool
async def get_declaration(ctx: RunContext):
    print(ctx.deps)
    policy =  {
        "name": "Asa Choi",
        "policyID": ctx.deps["policy_ID"],
        "gender": "M",
        "declaration": [
            {
                "name":"headache",
                "meaurement": {
                    "bloodpresure": 200
                }
            },
            {
                "name":"細菌性赤痢",
                "meaurement": {
                    "bloodpresure": 200
                }
            }
        ]

    }
    markdown = """
---

### **Radiology Report: Upper ABDOMEN, Liver Function Tests**

---

#### **Patient Information**
*   **Name:** [REDACTED]
*   **HN:** [REDACTED]
*   **Age:** 40 Years 5 Months 8 Days
*   **Gender:** Female

---

#### **Report Details**
- **Order Date:** 24/04/2024
- **Request By:** DR. DECHA WIMOL Chaidith
- **Report Type:** U/S UPPER ABDOMEN (ULTRASSО grabETRY OF Upper ABDOMEN)
- **History:** Follow up

---

#### **Findings**
*   **Liver:**
  - Normal size and smooth surface.
  - No space-taking lesion.
  - Multiple cysts scattering in the liver (0.4-4.3 cm).

Note: No evidence of portal hypertension or other complications (e.g., hemangion).

*   **Bile duct:**
  - No dilatation of IHD and CBD.

---

#### **Gallbladder**
*   **Gallbladder:**
  - Normal distension.
  - No gallstone.

Note: Two medium echogenicity nodules in the gallbladder wall (about 0.3 cm and 0.4 cm). These are suggestive of *gallbladder polyp*.     

*   **Pancreas:**
  - No visible pancreas.

---

#### **Spleen**
- Spleen is normal, parenchymal echogenicity present. No hydronephrosis or calcified cyst wall changes.

---

#### **Kidneys**
- Aorta: Normal size and parenchymal echogenicity, no hydronephrosis.
- Decreased size of a 0.6-cm hyperechoic lesion at lower pole left kidney (now about 0.9 cm).
- A bright lesion at lower pole left kidney (0.3 cm). This suggests possible renal stone or calcified cyst wall.

*   **Changes since last reported:**
  - No change due to hemangiomyolipoma of the lower pole left kidney.

---

#### **Aorta**
- Normal findings, no dilatation.

---

### **Conclusion**

1. Multiple cysts scattered in the liver (now about 0.4-4.3 cm).
2. Two medium echogenicity nodules in the gallbladder wall (about 0.3 cm and 0.4 cm), suggestive of *gallbladder polyp*.
3. Decreased size of a cyst at lower pole left kidney (now about 0.9 cm).
4. A bright lesion at lower pole left kidney (0.3 cm), possibly renal stone or calcified cyst wall.

---

### **Footnotes**

1. No hyperechoic lesion on the same findin.
2. Possibly hemangiomyolipoma."""
    return markdown

@assessmentAgent.tool_plain
async def get_web_info(declaration_name: str) -> str:
    print(Fore.BLACK, declaration_name)
    data =  await web_crawling("https://ganjoho.jp/public/cancer/liver/treatment.html")
    return data
 
async def web_crawling(url:str):   
    """
        craw the web and extract underwriting related concerns
    """
    class resultObj(BaseModel):
        checking_steps: list[str] = Field(description="Followup checking steps for underwriting")
        mortality: str = Field(description="mortality information, ideally with percentage for 10 year, 20 years and 30 years")
        symdroms: list[str]
        description: str
        reference_links: list[str]

    webagent = Agent(
        #"google-gla:gemini-2.0-flash-exp",
        "openai:gpt-4o-mini",
        deps_type=str,
        result_type=resultObj
    )
    

    import sys

    @webagent.tool
    async def getweb(ctx:RunContext, url: str) -> str:
        """
            get the information from web
        """
    
        crawler = AsyncWebCrawler()
        await crawler.start()
        result = await crawler.arun(
            url=ctx.deps,
        )
        await crawler.close()
        return result.markdown
    
    prompt = f"""You are an underwriter to extract key information from web for insurance underwriting use, all the information need to be extracted from the website directly, cannot make up the output"""
    result = await webagent.run(prompt, deps=url)
    return result.data

def main():
    result = assessmentAgent.run_sync(
        "get the summary of the application", 
        deps={
            "policy_ID": "123444"}
    )
    print(result.data)

main()
