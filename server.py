## pip install --upgrade google-genai==0.3.0##
import asyncio
import json
import os
import websockets
from google import genai
import base64
import random
# from db_operations import create_session ,store_conversation,transcribe_audio_gemini


# Load API key from environment
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBVbEoDEFMopCdj7P6NbGVv5_WfaZ0IQJA'
MODEL = "gemini-2.0-flash-exp"  # use your model ID

client = genai.Client(
  http_options={
    'api_version': 'v1alpha',
  }
)

# python -m http.server 8000

async def gemini_session_handler(client_websocket: websockets.WebSocketServerProtocol):
    """Handles the interaction with Gemini API within a websocket session.

    Args:
        client_websocket: The websocket connection to the client.
    """
    try:
        config_message = await client_websocket.recv()
        config_data = json.loads(config_message)
        config = config_data.get("setup", {})

        userData=config_data.get("userInfo")
        userId=userData["userId"]
        userName=userData["userName"]
        sessionId=userData["sessionId"]
        print(userData)    
        #create_session(userId,userName,sessionId)

        news_and_sentiment = {
        "global": {
            "US": {
                "key_events": [
                    "Upcoming Fed meeting on [Date] - Interest rate decision expected.",
                    "Ongoing debate about US fiscal spending and potential impact on inflation."
                ],
                "sentiment": "Mixed. Concerns about potential slowdown, but strong labor market provides some support."
            },
            "Geopolitics": {
                "key_events": [
                    "Continued tensions in [Region] - Monitoring impact on energy prices.",
                    "Uncertainty around [Country]'s political situation."
                ],
                "sentiment": "Negative. Geopolitical risks are elevated, increasing market volatility."
            },
            # Add other regions/factors as needed (e.g., China, EU)
        },
        "india": {
            "RBI": {
                "key_events": [
                    "Next RBI policy meeting on [Date] - Market anticipates potential policy stance.",
                    "RBI interventions in the currency market to manage volatility."
                ],
                "sentiment": "Cautious. Market watching RBI's response to inflation and global pressures."
            },
            "Economy": {
                "key_events": [
                    "Release of Q3 GDP data on [Date] - Expectations are...",
                    "Government announcement on new infrastructure projects."
                ],
                "sentiment": "Positive. Optimism around India's growth story, but some concerns about inflation."
            },
            # Add other factors (e.g., political developments)
        }
    }

        bank_report_context = {
            "summaries": [
                "India's economic outlook for 2025-26 is positive but navigating a complex global environment. GDP growth is expected to rise to 6.7% in FY26. Key drivers include recovering consumer spending, government infrastructure investment, and growth in the MSME and housing sectors. However, global economic slowdown, trade protectionism, and uneven private capex pose challenges. Inflation is expected to moderate, and the RBI may begin cutting rates. The external sector faces pressures from potential trade restrictions and fluctuations in capital flows.",
                "Key macroeconomic forecasts include: Real GDP growth of 6.4% in FY25 and 6.7% in FY26; CPI inflation averaging 5.0% in FY25 and 4.3% in FY26; and USD/INR exchange rate in the range of 85-86 by end of FY25 and 86-87 by end of FY26. Private consumption is shifting towards rural demand, supported by income support schemes and increased women's labor force participation. Investment growth is driven by government capex, but private capex remains uneven. The current account deficit is projected to be 1.5% of GDP in FY25 and 1.0% in FY26."
            ],
            "retrieved_chunks": [
                "India is expected to grow at 6.7% in 2025-26 up from 6.4% in 2024-25. Consumer spending is expected to recover, primarily through a push from higher rural demand while urban demand continues to 'mean-revert'. A moderation in inflation is expected to help support discretionary demand both in rural and urban areas. Moreover, hiring intentions have started improving in the formal job market. This combined with government infrastructure spending, growth in the MSME segment and a continued upturn in the housing market is likely to support employment elsewhere. Lastly, a rise in women labour force participation in rural areas, improvement in standard of living at the bottom of the pyramid and cash transfers under various schemes by the government is likely to help repair household balance sheets and spur demand on a more sustained basis.",
                "Real GDP growth is projected at 6.4% for FY25 and 6.7% for FY26. Real GVA growth is projected at 6.4% for FY25 and 6.5% for FY26. Private consumption growth is expected to be 7.1% in FY25 and 7.5% in FY26. Investment growth is forecasted at 7.0% for FY25 and 7.2% for FY26. Exports (goods and services) growth is projected to be 7.5% in FY25 and 9.5% in FY26. Manufacturing growth is expected to be 2.6% in FY25 and 7.7% in FY26. Services growth is projected at 8.3% in FY25 and 5.6% in FY26. Nominal GDP growth is expected to be 10.1% in FY25 and 10.9% in FY26. CPI inflation is projected to average 5.0% in FY25 and 4.3% in FY26. Core inflation is expected to average 3.6% in FY25 and 4.5% in FY26. The current account deficit is projected to be 1.5% of GDP in FY25 and 1.0% of GDP in FY26. The fiscal deficit is projected to be 4.9% of GDP in FY25 and 4.5% in FY26. The RBI's repo rate is expected to be 6.5% in FY25 and 5.8% in FY26. The USD/INR exchange rate is projected to be in the range of 85-86 by the end of FY25 and 86-87 by the end of FY26.",
                "We expect the current account deficit (CAD) for FY25 to stand at 1.5% of GDP and at 1.0% of GDP in FY26. This assumes average crude oil price at USD 70-75 pbl. and gold prices to average at USD 2800 oz. in FY26. Narrowing of current account deficit in FY26 is likely to be led by higher services exports (net) and remittances, and a slowdown in crude oil imports as oil prices trend lower on excess global supply. However, export growth is anticipated to remain subdued due to a slowdown in India’s key trading partners and the influence of rising trade protectionist policies ('The Trump effect')."
            ],
            "key_forecasts": {
                "Real GDP Growth (FY25)": "6.4%",
                "Real GDP Growth (FY26)": "6.7%",
                "CPI Inflation (FY25)": "5.0%",
                "CPI Inflation (FY26)": "4.3%",
                "USD/INR (FY25)": "85-86 (eop)",
                "USD/INR (FY26)": "86-87 (eop)",
                "Current Account Deficit (% of GDP, FY25)": "1.5%",
                "Current Account Deficit (% of GDP, FY26)": "1.0%"
            },
            "consumption_drivers": {
                "Rural Demand Factors": [
                    "Higher MSPs",
                    "Normal monsoons",
                    "Lower input costs",
                    "Direct income support schemes",
                    "Increased women labor force participation"
                ],
                "Urban Demand Trends": [
                    "Normalization of pent-up demand",
                    "Recovery in hiring intentions",
                    "Push to employment from MSME sector",
                    "Infrastructure spending by government",
                    "Easing monetary policy"
                ]
            },
            "investment_drivers": {
                "Government Capex Focus": [
                    "Roads and highways",
                    "Modernization of railways",
                    "Ports",
                    "Housing and logistics"
                ],
                "Private Capex Trends": [
                    "MSME capacity expansion",
                    "Services sector growth (hospitality, restaurants, real estate, health, education)"
                ]
            },
            "trade_risks": {
                "Protectionist Policies Impact": [
                    "Potential for tariffs/restrictions from US",
                    "Impact on India's exports, particularly pharmaceuticals, textiles, and engineering goods",
                    "Risk to global growth and trade"
                ]
            }
        }

        config["system_instruction"] = """
                You are a specialized assistant for forex currency exchange forecasting during screen-sharing sessions. Your role is to:

                1)  Analyze and describe forex market trends based on the shared content (e.g., currency charts, trading platforms).
                2)  Incorporate data from the provided `bank_report_context` to extract key financial insights and macroeconomic indicators. Pay close attention to the `key_forecasts`, `consumption_drivers`, `investment_drivers`, and `trade_risks` sections.
                3)  Integrate relevant news and market sentiment from the `news_and_sentiment` data to assess potential market-moving events.
                4)  Use bank report insights, news analysis, and market sentiment to generate short-term forex forecasts for relevant currency pairs.
                5)  Provide clear explanations of technical and fundamental factors influencing currency movements. When explaining fundamental factors, refer to the data within `bank_report_context` and `news_and_sentiment` to support your analysis.
                6)  Assist with interpreting financial charts, reports, and forex trading platforms.
                7)  Maintain a professional, data-driven, and concise approach to deliver actionable insights.

                Here's how to use the `bank_report_context`:

                * `summaries`: Use these for a quick overview of the bank report's main points.
                * `retrieved_chunks`: These provide more detailed information and data. Prioritize this information.
                * `key_forecasts`: Refer to these for specific numerical forecasts (e.g., GDP growth, inflation, exchange rates).
                * `consumption_drivers`: Use these to understand factors influencing consumer spending trends.
                * `investment_drivers`: Use these to analyze investment trends and drivers.
                * `trade_risks`: Pay attention to these for potential risks related to trade and the global economy.

                Here's how to use the `news_and_sentiment`:

                * `global`: This section contains news and sentiment related to major global factors (e.g., US, Geopolitics).
                * `india`: This section contains news and sentiment specific to India (e.g., RBI, Economy).
                * `key_events`: These are specific upcoming events or ongoing situations that could impact the market.
                * `sentiment`: This is a general overview of the prevailing market mood related to that factor.

                Bank Report Context: {bank_report_context}

                News and Sentiment: {news_and_sentiment}
                """


        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected to Gemini API")

            async def send_to_gemini():
                """Sends messages from the client websocket to the Gemini API."""
                try:
                  async for message in client_websocket:
                      try:
                          data = json.loads(message)
                          #get sessionId  from user
                          if "realtime_input" in data:
                              for chunk in data["realtime_input"]["media_chunks"]:
                                  if chunk["mime_type"] == "audio/pcm":
                                      await session.send({"mime_type": "audio/pcm", "data": chunk["data"]})
                                      # user: 
                                      # gemini : 
                                      
                                  elif chunk["mime_type"] == "image/jpeg":
                                      print('Image is received from ')
                                      await session.send({"mime_type": "image/jpeg", "data": chunk["data"]})
                                      
                      except Exception as e:
                          print(f"Error sending to Gemini: {e}")
                  print("Client connection closed (send)")
                except Exception as e:
                     print(f"Error sending to Gemini: {e}")
                finally:
                   print("send_to_gemini closed")


            async def receive_from_gemini():
                """Receives responses from the Gemini API and forwards them to the client, looping until turn is complete."""
                try:
                    while True:
                        try:
                            print("receiving from gemini")
                            async for response in session.receive():
                                if response.server_content is None:
                                    print(f'Unhandled server message! - {response}')
                                    continue

                                model_turn = response.server_content.model_turn
                                if model_turn:
                                    for part in model_turn.parts:
                                        if hasattr(part, 'text') and part.text is not None:
                                            await client_websocket.send(json.dumps({"text": part.text}))
                                        elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                            print("audio mime_type:", part.inline_data.mime_type)
                                            base64_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                            await client_websocket.send(json.dumps({
                                                "audio": base64_audio,
                                            }))
                                            print("audio received")

                                if response.server_content.turn_complete:
                                    print('\n<Turn complete>')
                        except websockets.exceptions.ConnectionClosedOK:
                            print("Client connection closed normally (receive)")
                            break  # Exit the loop if the connection is closed
                        except Exception as e:
                            print(f"Error receiving from Gemini: {e}")
                            break 

                except Exception as e:
                      print(f"Error receiving from Gemini: {e}")
                finally:
                      print("Gemini connection closed (receive)")


            # Start send loop
            send_task = asyncio.create_task(send_to_gemini())
            # Launch receive loop as a background task
            receive_task = asyncio.create_task(receive_from_gemini())
            await asyncio.gather(send_task, receive_task)


    except Exception as e:
        print(f"Error in Gemini session: {e}")
    finally:
        print("Gemini session closed.")
        return None



async def main() -> None:
    async with websockets.serve(gemini_session_handler, "localhost", 9083):
        print("Running websocket server localhost:9083...")
        await asyncio.Future()  # Keep the server running indefinitely


if __name__ == "__main__":
    asyncio.run(main())