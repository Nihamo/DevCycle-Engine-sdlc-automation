import { Check, X } from "lucide-react"
import { useLocation } from "react-router-dom"
import type { QATesting } from "../types";
import { useEffect, useState } from "react";
import { BACKEND_URL } from "../../config";
import Loading from "../components/Loading";
import ToastError from "../components/ToastError";

export default function QATesting() {

    const location = useLocation();
    const data = location.state?.data;
    const [loading, setLoading] = useState(true);

    const [qaTesting, setQaTesting] = useState<QATesting>({
        qaTesting: [],
    })

    // const dummyCases = [
    //     {
    //         test_id: "TC-002",
    //         description: "Verify user login functionality with valid credentials",
    //         steps: [
    //             "Navigate to login page",
    //             "Enter valid credentials",
    //             "Click login and verify dashboard loads"
    //         ],
    //         status: "fail",
    //     },
    //     {
    //         test_id: "TC-004",
    //         description: "Test checkout process with invalid payment",
    //         steps: [
    //             "Proceed to checkout",
    //             "Enter invalid card details",
    //             "Verify error message shown"
    //         ],
    //         status: "fail",
    //     },
    //     {
    //         test_id: "TC-003",
    //         description: "Check add-to-cart functionality on product listing",
    //         steps: [
    //             "Open product listing",
    //             "Click 'Add to Cart'",
    //             "Verify cart count and item in cart page"
    //         ],
    //         status: "pass",
    //     },
    // ];

    const getQaTesting = async () => {
        setLoading(true);
        try {
            if (!data?.session_id) {
                throw new Error("Session ID is missing");
            }

            const response = await fetch(`${BACKEND_URL}/qa/testing/get/${data.session_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });


            if (!response.ok) {
                throw new Error("failed to call /qa/testing/get/{{session_id}}");
            }

            const qa_testing_response = await response.json();

            // console.log(qa_testing_response.test_cases);
            setQaTesting({
                qaTesting: [
                    ...qa_testing_response.test_cases,
                    // ...dummyCases,
                ],
            })

            setLoading(false);

        } catch (error) {
            console.log("error calling /qa/testing/get/{{session_id}}")
            setLoading(false);
            ToastError(error)
        }
    }


    useEffect(() => {
        getQaTesting();
    }, [])


    if(loading) {
        return <Loading />
    }

    return (
        <div className="flex-1 p-6 overflow-y-auto bg-gray-900">
            <div className="max-w-6xl mx-auto px-2">
                <p className="text-xl font-semibold">
                    QA Testing
                </p>
                <p className="text-sm pt-1 text-gray-400 font-medium">
                    Comprehensive quality assurance testing of the application to identify bugs and issues.
                </p>
            </div>
            <div className="max-w-6xl mx-auto py-6">
                <div className="bg-gray-700 rounded-lg shadow-xl p-5 border border-gray-400">
                    <div className="py-4 grid grid-cols-1 md:grid-cols-2 gap-4 mx-4">
                        {qaTesting.qaTesting && qaTesting.qaTesting.map((qaTest, index) => (
                            <div
                                key={index}
                                className="flex flex-col p-2 bg-gradient-to-b from-blue-950 via-blue-900 to-blue-800
                                        rounded-lg hover:scale-[1.01]"
                            >
                                <div className="flex items-center justify-between p-2">
                                    <p className="text-lg font-semibold">{qaTest.test_id}</p>
                                    <p
                                        className={`flex items-center justify-center gap-1
                                            ${qaTest.status === 'pass' ? 'bg-green-600 text-green-200' : 'bg-red-600 text-red-200'}
                                            px-2 py-1 rounded-full hover:scale-[1.02] font-semibold
                                            shadow-sm shadow-slate-900`}
                                    >
                                        {qaTest.status === "pass" ? (<>
                                            <Check className="w-5 h-5" />
                                            Pass
                                        </>) :
                                            (<>
                                                <X className="w-5 h-5" />
                                                Fail
                                            </>)
                                        }
                                    </p>
                                </div>
                                <hr className="my-5 mx-2 border-t-2 rounded-full border-blue-400" />
                                <div className="p-2 flex">
                                    <p
                                        className={`flex flex-wrap gap-1 items-center justify-start 
                                        font-medium ${qaTest.status === 'pass' ? 'text-green-100' : 'text-red-100'}`}
                                    >
                                        <span
                                            className={`${qaTest.status === 'pass' ? 'text-green-400' : 'text-red-400'} 
                                            font-semibold text-sm inline`}
                                        >
                                            {qaTest.status === 'pass' ? 'Test Passed Successfully' : 'Test Failed'}:
                                        </span>
                                        <span className="inline">
                                            {qaTest.description}
                                        </span>
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}