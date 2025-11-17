import { ShieldAlert } from "lucide-react";
import { Review } from "../types"


interface SecurityReviewCardProps {
    review: Review;
    priorityStyle: {
        box: string;
        smallBox: string;
        badge: string;
        text: string;
        line: string;
    }
}


export default function SecurityReviewCard({ review, priorityStyle }: SecurityReviewCardProps) {


    return (
        <div className={`flex flex-col p-2 bg-gradient-to-b ${priorityStyle.box} rounded-lg hover:scale-[1.01]`}>
            <div className="flex items-center justify-between px-2">
                <div
                    className={`flex w-fit gap-1 ${priorityStyle.badge} p-2
                                                rounded-full text-xs font-bold items-center justify-center m-2`}
                >
                    <ShieldAlert className="w-3" />
                    <p className="">{review.sec_id}</p>
                </div>
                <p
                    className="py-1 px-2 w-fit rounded-full bg-orange-600 text-center
                                                    text-xs font-semibold uppercase"
                >
                    {review.priority}
                </p>
            </div>
            <p className={`p-2 font-medium ${priorityStyle.text}`}>
                {review.review}
            </p>
            <div className={`flex flex-col mx-2 p-3 ${priorityStyle.smallBox} rounded-lg`}>
                <p className="text-gray-400 font-semibold text-sm">Location:</p>
                <p className="mt-1 text-gray-200 font-medium">{review.file_path}</p>
            </div>
            <hr className={`my-4 mx-2 border-t-2 ${priorityStyle.line} rounded-full`} />
            <div className="px-2 pb-2">
                <p className={`${priorityStyle.text} font-semibold`}>Recommendation</p>
                <p className="font-normal text-sm">{review.recommendation}</p>
            </div>
        </div>
    )
}