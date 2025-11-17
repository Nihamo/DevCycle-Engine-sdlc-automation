import React, { useState } from "react"
import { useLocation } from "react-router-dom"
import type { TestCases } from "../types";
import { BACKEND_URL } from "../../config";
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";



export default function TestCases() {

    const location = useLocation();
    const data = location.state?.data;
    const [loading, setLoading] = useState(true);

    const [testCases, setTestCases] = useState<TestCases>({
        testCases: [],
    })


    const getTestCases = async () => {
        setLoading(true);
        if (location.state?.["testing"]?.test_cases) {
            console.log("test cases inside");
            setTestCases({
                testCases: location.state?.["testing"]?.test_cases,
            })
            setLoading(false);
            return
        }
        try {
            console.log("test cases outside")
            if (!data?.session_id) {
                throw new Error("Session ID is missing");
            }

            const response = await fetch(`${BACKEND_URL}/test/cases/get/${data.session_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("failed to call /test/cases/get/{{session_id}}")
            }

            const test_cases_response = await response.json();
            // console.log(test_cases_response.test_cases);
            setTestCases({
                testCases: test_cases_response.test_cases,
            })
            setLoading(false);

        } catch (error) {
            console.log("error calling /test/cases/get/{{session_id}}")
            setLoading(false);
            ToastError(error)
        }
    }

    React.useEffect(() => {
        getTestCases();
    }, [location.state])


    if(loading) {
        return <Loading />
    }

    return (
        <div
            className="flex-1 p-6 overflow-y-auto bg-gray-900"
        >
            <div className="max-w-6xl mx-auto px-2">
                <p
                    className="text-xl font-semibold"
                >
                    Test Cases
                </p>
                <p
                    className="text-sm pt-1 text-gray-400 font-medium"
                >
                    The AI generated test cases for your application.
                </p>
            </div>
            <div className="max-w-6xl mx-auto py-6">
                <div className="bg-gray-700 rounded-lg shadow-xl p-5 border border-gray-400">
                    <div className="py-4 flex flex-col gap-6">
                        {testCases.testCases && testCases.testCases.map((testCase, index) => (
                            <div
                                key={index}
                                className="flex flex-col p-2 bg-gradient-to-b from-blue-950 via-blue-900 to-blue-800 rounded-lg hover:scale-[1.01]"
                            >
                                <div className="flex gap-2 px-2">
                                    <p className="">{testCase.test_id}:</p>
                                    <p className="">{testCase.description}</p>
                                </div>
                                <hr className="my-5 mx-2 border-t-2 rounded-full border-gray-400" />
                                <div className="p-2 flex flex-col">
                                    <p className="font-semibold text-lg">Steps:</p>
                                    <div className="flex flex-col px-2">
                                        {testCase.steps.map((step, stepIndex) => (
                                            <p className="py-1 text-sm font-medium text-gray-300">{stepIndex + 1}. {step}</p>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}